
import pyaes
import hashlib


def is_bip38_available(require_fast=True):
    ''' Returns True iff we have the underlying libs to decode Bip38 (scrypt libs).
    Use require_fast=True if we require native code.  Note that the non-native
    code libs are incredibly slow and not suitable for production use. '''
    if not Bip38Key.canDecrypt():
        return False
    if require_fast and not Bip38Key.isFast():
        return False
    return True

def is_bip38_key(bip38str, *, net=None):
    ''' Returns True iff the '6P...' passed-in string is a valid Bip38 encrypted
    key. False otherwise.  Does not require is_bip38_available to return a valid
    result. '''
    return Bip38Key.isBip38(bip38str, net=net)

def bip38_decrypt(enc_key, password, *, require_fast=True, net=None):
    ''' Pass a bip38 key eg '6PnQ46rtBGW4XuiudqinAZYobT4Aa8GdtYkjG1LvXK3RBq6ARJA3txjj21'
    and a password. Both should be str's. Returns a tuple of:
    (decrypted_WIF_key_str, Address_object) if decoding succeeds, or an empty
    tuple on bad password.  Returns 'None' if failed due to missing libs or
    because of malformed key. Use is_bip38_available() to determine if we
    actually can decode bip38 keys (we have the libs). '''
    if not is_bip38_available(require_fast):
        return None
    try:
        return Bip38Key(enc_key, net=net).decrypt(password)
    except Bip38Key.PasswordError:
        return tuple()  # Bad password result is an empty tuple
    except Bip38Key.Error as e:
        raise Exception("[bip38_decrypt] Error with key", enc_key, "error was:", repr(e))
    # return None


class Bip38Key:
    '''
        Implements Bip38 _encrypt_ and _decrypt_ functionality.

        Supports both ECMult and NonECMult key types, so it should work with
        all BIP38 keys.

        This code was translated from Calin's Go implementation of brute38:
        https://www.github.com/cculianu/brute38

        Note that to actually encrypt or decrypt keys you need either:

        - hashlib.scrypt (python 3.6 + openssl 1.1) which is very fast.
        - Cryptodome.Protocol.KDF.scrypt (also fast as it's native)
        - Or, the slow python-only lib 'pyscrypt' which is INCREDIBLY slow.

        Use Bip38Key.canDecrypt() to test if the decrypt() functionality
        is actually available (that is, if we found a scrypt implementation).

        Similarly, use Bip38Key.canEncrypt() to test whether encryption works.

        Use Bip38Key.isFast() to determine if decrypt() will be fast or
        painfully slow: It can take several minutes to decode a single key
        if Bip38Key.isFast() is False.

        Example psueodo-UI code to use this class in a manner than won't drive
        users crazy:

        if Bip38Key.isBip38(userKey): # test that user input is a bip38 key
            if not Bip38Key.canDecrypt():
                # show some GUI error that scrypt is missing here...
                gui.warning("You supplied a bip38 key but no scrypt lib is found!")
                return
            if not Bip38Key.isFast():
                # warn user here that the operation will take MINUTES!
                if not gui.question("The operation will be slow.. continue?"):
                    return # user opted out.
                gui.pop_up_waiting_dialog() # show user a spining waiting thing...

            try:
                pass = gui.get_password("Please enter the password for this bip38 key.")
                wif, addr = Bip38Key(userKey).decrypt(pass) # may be fast or slow depending on underlying lib...
            except Bip38Key.PasswordError:
                # user supplied a bad password ...
                gui.show_error("Invalid password!")
                return
            finally:
                if not Bip38Key.isFast(): gui.hide_waiting_dialog() # hide waiting dialog if shown...

            gui.show(wif, addr) # show WIF key and address in GUI here
        '''
    class Type:
        NonECMult = 0x42
        ECMult    = 0x43
        Unknown   = 0x0

    enc = "" # string // bip38 base58 encoded key (as the user would see it in a paper wallet)
    dec = b'' # []byte // key decoded to bytes (still in encrypted form)
    flag = 0x0 # byte // the flag byte
    compressed = False # bool // boolean flag determining if compressed
    typ = Type.Unknown # KeyType // one of NonECMultKey or ECMultKey above
    salt = b'' # [] byte // the slice salt -- a slice of .dec slice
    entropy = b'' # [] byte // only non-nil for typ==ECMultKey -- a slice into .dec
    hasLotSequence = False # bool // usually false, may be true only for typ==ECMultKey

    #// coin / network specific info affecting key decription and address decoding:
    # this gets populated by current value of NetworkConstants.net.WIF_PREFIX, etc
    networkVersion   = 0x00 # byte // usually 0x0 for BTC/BCH
    privateKeyPrefix = 0x80 # byte // usually 0x80 for BTC/BCH

    # Internal class-level vars
    _scrypt_1 = None
    _scrypt_2 = None

    class Error(Exception):
        ''' Decoding a BIP38 key will raise a subclass of this '''
        pass

    class DecodeError(Error):
        pass

    class PasswordError(Error, Exception):
        pass

    def __init__(self, enc, *, net=None):
        if isinstance(enc, (bytearray, bytes)):
            enc = enc.decode('ascii')
        assert isinstance(enc, str), "Bip38Key must be instantiated with an encrypted bip38 key string!"
        if not enc.startswith('6P'):
            raise Bip38Key.DecodeError("Provided bip38 key string appears to not be valid. Expected a '6P' prefix!")
        self.net = networks.net if net is None else net
        self.enc = enc
        self.dec = DecodeBase58Check(self.enc)
        if not self.dec:
            raise Bip38Key.DecodeError('Cannot decode bip38 key: Failed Base58 Decode Check')
        if len(self.dec) != 39:
            raise Bip38Key.DecodeError('Cannot decode bip38 key: Resulting decoded bytes are of the wrong length (should be 39, is {})'.format(len(self.dec)))
        if self.dec[0] == 0x01 and self.dec[1] == 0x42:
            self.typ = Bip38Key.Type.NonECMult
        elif self.dec[0] == 0x01 and self.dec[1] == 0x43:
            self.typ = Bip38Key.Type.ECMult
        else:
            raise Bip38Key.DecodeError("Malformed byte slice -- the specified key appears to be invalid")

        self.flag = self.dec[2]
        self.compressed = False
        if self.typ == Bip38Key.Type.NonECMult:
            self.compressed = self.flag == 0xe0
            self.salt = self.dec[3:7]
            if not self.compressed and self.flag != 0xc0:
                raise Bip38Key.DecodeError("Invalid BIP38 compression flag")
        elif self.typ == Bip38Key.Type.ECMult:
            self.compressed = (self.flag&0x20) != 0
            self.hasLotSequence = (self.flag&0x04) != 0
            if (self.flag & 0x24) != self.flag:
                raise Bip38Key.DecodeError("Invalid BIP38 ECMultKey flag")
            if self.hasLotSequence:
                self.salt = self.dec[7:11]
                self.entropy = self.dec[7:15]
            else:
                self.salt = self.dec[7:15]
                self.entropy = self.salt

        self.networkVersion, self.privateKeyPrefix = self.net.ADDRTYPE_P2PKH, self.net.WIF_PREFIX

    @property
    def lot(self) -> int:
        ''' Returns the 'lot' number if 'hasLotSequence' or None otherwise. '''
        if self.dec and self.hasLotSequence:
            return self.entropy[4] * 4096 + self.entropy[5] * 16 + self.entropy[6] // 16;

    @property
    def sequence(self) -> int:
        ''' Returns the 'sequence' number if 'hasLotSequence' or None
        otherwise. '''
        if self.dec and self.hasLotSequence:
            return (self.entropy[6] & 0x0f) * 256 + self.entropy[7]

    def typeString(self):
        if self.typ == Bip38Key.Type.NonECMult: return "NonECMultKey"
        if self.typ == Bip38Key.Type.ECMult: return "ECMultKey"
        return "UnknownKey"

    @classmethod
    def isBip38(cls, bip38_enc_key, *, net=None):
        ''' Returns true if the encryped key string is a valid bip38 key. '''
        try:
            cls(bip38_enc_key, net=net)
            return True # if we get to this point the key was successfully decoded.
        except cls.Error as e:
            #print_error("[Bip38Key.isBip38] {}:".format(bip38_enc_key), e)
            return False

    @staticmethod
    def isFast():
        ''' Returns True if the fast hashlib.scrypt implementation is found. '''
        cls = __class__
        if cls._scrypt_1 or cls._scrypt_2:
            return True
        if hasattr(hashlib, 'scrypt'):
            print_error("[{}] found and using hashlib.scrypt! (Fast scrypt)".format(cls.__name__))
            cls._scrypt_1 = hashlib.scrypt
            return True
        else:
            try:
                from Cryptodome.Protocol.KDF import scrypt
                cls._scrypt_2 = scrypt
                print_error("[{}] found and using Cryptodome.Protocol.KDF.scrypt! (Fast scrypt)".format(cls.__name__))
                return True
            except (ImportError, NameError):
                pass
        return False

    @staticmethod
    def canDecrypt():
        ''' Tests if this class can decrypt. If this returns False then we are
        missing the scrypt module: either hashlib.scrypt or pyscrypt '''
        if Bip38Key.isFast():
            return True
        try:
            import pyscrypt
            return True
        except ImportError:
            pass
        return False

    @staticmethod
    def canEncrypt(): return Bip38Key.canDecrypt()

    @staticmethod
    @profiler
    def _scrypt(password, salt, N, r, p, dkLen):
        password = to_bytes(password)
        salt = to_bytes(salt)
        if Bip38Key.isFast():
            if __class__._scrypt_1:
                return __class__._scrypt_1(password = password, salt = salt, n=N, r=r, p=p, dklen=dkLen)
            elif __class__._scrypt_2:
                return __class__._scrypt_2(password = password, salt = salt, N=N, r=r, p=p, key_len=dkLen)
            raise RuntimeError("INTERNAL ERROR -- neither _scrypt_1 or _scrypt_2 are defined, but isFast()==True... FIXME!")
        try:
            import pyscrypt
        except ImportError:
            raise Bip38Key.Error("We lack a module to decrypt BIP38 Keys.  Install either: Cryptodome (fast), Python + OpenSSL 1.1 (fast), or pyscrypt (slow)")
        print_error("[{}] using slow pyscrypt.hash... :(".format(__class__.__name__))
        return pyscrypt.hash(password = password, salt = salt, N=N, r=r, p=p, dkLen=dkLen)

    def _decryptNoEC(self, passphrase : str) -> tuple: # returns the (WIF private key, Address)  on success, raises Error on failure.
        scryptBuf = Bip38Key._scrypt(password = passphrase, salt = self.salt, N=16384, r=8, p=8, dkLen=64)
        derivedHalf1 = scryptBuf[0:32]
        derivedHalf2 = scryptBuf[32:64]
        encryptedHalf1 = self.dec[7:23]
        encryptedHalf2 = self.dec[23:39]

        h = pyaes.AESModeOfOperationECB(derivedHalf2)
        k1 = h.decrypt(encryptedHalf1)
        k2 = h.decrypt(encryptedHalf2)

        keyBytes = bytearray(32)
        for i in range(16):
            keyBytes[i] = k1[i] ^ derivedHalf1[i]
            keyBytes[i+16] = k2[i] ^ derivedHalf1[i+16]
        keyBytes = bytes(keyBytes)

        eckey = regenerate_key(keyBytes)

        pubKey = eckey.GetPubKey(self.compressed)

        from .address import Address

        addr = Address.from_pubkey(pubKey)
        addrHashed = Hash(addr.to_storage_string(net=self.net))[0:4]

        assert len(addrHashed) == len(self.salt)

        for i in range(len(addrHashed)):
            if addrHashed[i] != self.salt[i]:
                raise Bip38Key.PasswordError('Supplied password failed to decrypt bip38 key.')

        return serialize_privkey(keyBytes, self.compressed, 'p2pkh', net=self.net), addr

    @staticmethod
    def _normalizeNFC(s : str) -> str:
        '''Ensures unicode string is normalized to NFC standard as specified by bip38 '''
        import unicodedata
        return unicodedata.normalize('NFC', s)

    def decrypt(self, passphrase : str) -> Tuple[str, object]: # returns the (wifkey string, Address object)
        assert isinstance(passphrase, str), "Passphrase must be a string!"
        passphrase = self._normalizeNFC(passphrase)  # ensure unicode bytes are normalized to NFC standard as specified by bip38
        if self.typ == Bip38Key.Type.NonECMult:
            return self._decryptNoEC(passphrase)
        elif self.typ != Bip38Key.Type.ECMult:
            raise Bip38Key.Error("INTERNAL ERROR: Unknown key type")

        prefactorA = Bip38Key._scrypt(password = passphrase, salt = self.salt, N=16384, r=8, p=8, dkLen=32)

        if self.hasLotSequence:
            prefactorB = prefactorA + self.entropy
            passFactor = Hash(prefactorB)
            del prefactorB
        else:
            passFactor = prefactorA

        ignored, passpoint = get_pubkeys_from_secret(passFactor)

        encryptedpart1 = self.dec[15:23]
        encryptedpart2 = self.dec[23:39]

        derived = Bip38Key._scrypt(password = passpoint, salt = self.dec[3:7] + self.entropy, N=1024, r=1, p=1, dkLen=64)

        h = pyaes.AESModeOfOperationECB(derived[32:])

        unencryptedpart2 = bytearray(h.decrypt(encryptedpart2))
        for i in range(len(unencryptedpart2)):
            unencryptedpart2[i] ^= derived[i+16]

        encryptedpart1 += bytes(unencryptedpart2[:8])

        unencryptedpart1 = bytearray(h.decrypt(encryptedpart1))

        for i in range(len(unencryptedpart1)):
            unencryptedpart1[i] ^= derived[i]

        seeddb = bytes(unencryptedpart1[:16]) + bytes(unencryptedpart2[8:])
        factorb = Hash(seeddb)

        bytes_to_int = Bip38Key._bytes_to_int

        passFactorI = bytes_to_int(passFactor)
        factorbI = bytes_to_int(factorb)

        privKey = passFactorI * factorbI
        privKey = privKey % 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

        int_to_bytes = Bip38Key._int_to_bytes

        privKey = int_to_bytes(privKey, 32)

        eckey = regenerate_key(privKey)

        pubKey = eckey.GetPubKey(self.compressed)

        from .address import Address

        addr = Address.from_pubkey(pubKey)
        addrHashed = Hash(addr.to_storage_string(net=self.net))[0:4]

        for i in range(len(addrHashed)):
            if addrHashed[i] != self.dec[3+i]:
                raise Bip38Key.PasswordError('Supplied password failed to decrypt bip38 key.')


        return serialize_privkey(privKey, self.compressed, 'p2pkh', net=self.net), addr

    @classmethod
    def encrypt(cls, wif : str, passphrase : str, *, net=None) -> object:
        ''' Returns a Bip38Key instance encapsulating the supplied WIF key
        encrypted with passphrase. May raise on bad/garbage WIF or other bad
        arguments. '''
        assert cls.canEncrypt(), "scrypt function missing. Cannot encrypt."
        assert isinstance(passphrase, str), "Passphrase must be a string!"
        if net is None: net = networks.net
        _type, key_bytes, compressed = deserialize_privkey(wif, net=net)  # may raise
        if _type != 'p2pkh':
            raise ValueError('Only p2pkh WIF keys may be encrypted using BIP38 at this time.')
        public_key = public_key_from_private_key(key_bytes, compressed)
        addr_str = pubkey_to_address(_type, public_key, net=net)
        addr_hash = Hash(addr_str)[0:4]
        passphrase = cls._normalizeNFC(passphrase)  # ensure unicode bytes are normalized to NFC standard as specified by bip38

        derived_key = cls._scrypt(passphrase, addr_hash, N=16384, r=8, p=8, dkLen=64)

        derivedHalf1 = derived_key[:32]
        derivedHalf2 = derived_key[32:]

        h = pyaes.AESModeOfOperationECB(derivedHalf2)

        # Encrypt bitcoinprivkey[0...15] xor derivedhalf1[0...15]
        encryptedHalf1 = h.encrypt(bytes( (x[0] ^ x[1]) for x in zip(key_bytes[:16], derivedHalf1[:16])) )
        encryptedHalf2 = h.encrypt(bytes( (x[0] ^ x[1]) for x in zip(key_bytes[16:], derivedHalf1[16:])) )

        flag = 0xe0 if compressed else 0xc0
        b38 = bytes((0x01, cls.Type.NonECMult)) + bytes((flag,)) + to_bytes(addr_hash) + encryptedHalf1 + encryptedHalf2

        return cls(EncodeBase58Check(b38))


    _ec_mult_magic_prefix = bytes.fromhex('2CE9B3E1FF39E2')

    @classmethod
    def createECMult(cls, passphrase : str, lot_sequence : Tuple[int, int] = None,
                     compressed = True, *, net=None) -> object:
        ''' Creates a new, randomly generated and encrypted "EC Mult" Bip38 key
        as per the Bip38 spec. The new key may be decrypted later with the
        supplied passphrase to yield a 'p2pkh' WIF private key.

        May raise if the scrypt function is missing.

        Optional arguments:

        `lot_sequence`, a tuple of (lot, sequence), both ints, with lot being an
        int in the range [0,1048575], and sequence being an int in the range
        [0, 4095]. This tuple, if specified, will be encoded in the generated
        Bip38 key as the .lot and .sequence property.

        `compressed` specifies whether to encode a compressed or uncompressed
        bitcoin pub/priv key pair. Older wallets do not support compressed keys
        but all new wallets do.'''
        assert cls.canEncrypt(), "scrypt function missing. Cannot encrypt."
        assert isinstance(passphrase, str), "Passphrase must be a string!"
        if net is None: net = networks.net
        passphrase = cls._normalizeNFC(passphrase)

        has_lot_seq = lot_sequence is not None

        if not has_lot_seq:
            # No lot_sequence
            ownersalt = ownerentropy = to_bytes(os.urandom(8))
            magic = cls._ec_mult_magic_prefix + bytes((0x53,))
        else:
            lot, seq = lot_sequence
            assert 0 <= lot <= 1048575, "Lot number out of range"
            assert 0 <= seq <= 4095, "Sequence number out of range"

            ownersalt = to_bytes(os.urandom(4))
            lotseq = int(lot * 4096 + seq).to_bytes(4, byteorder='big')
            ownerentropy = ownersalt + lotseq
            magic = cls._ec_mult_magic_prefix + bytes((0x51,))

        prefactor = cls._scrypt(passphrase, salt=ownersalt, N=16384, r=8, p=8, dkLen=32)

        if has_lot_seq:
            passfactor = Hash(prefactor + ownerentropy)
        else:
            passfactor = prefactor

        ignored, passpoint = get_pubkeys_from_secret(passfactor)

        intermediate_passphrase_string = magic + ownerentropy + passpoint # 49 bytes (not a str, despite name. We use the name from bip38 spec here)

        enc = EncodeBase58Check(intermediate_passphrase_string)
        print_error("[{}] Intermediate passphrase string:".format(cls.__name__), enc)
        return cls.ec_mult_from_intermediate_passphrase_string(enc, compressed)

    @classmethod
    def ec_mult_from_intermediate_passphrase_string(cls, enc_ips : bytes,
                                                    compressed = True) -> object:
        ''' Takes a Bip38 intermediate passphrase string as specified in the
        bip38 spec and generates a random and encrypted key, returning a newly
        constructed Bip38Key instance. '''
        ips = DecodeBase58Check(enc_ips)
        assert ips.startswith(cls._ec_mult_magic_prefix), "Bad intermediate string"
        hls_byte = ips[7]
        assert hls_byte in (0x51, 0x53), "Bad has_lot_seq byte"
        has_lot_seq = hls_byte == 0x51
        ownerentropy = ips[8:16] # 8 bytes
        passpoint = ips[16:]  # 33 bytes

        assert len(passpoint) == 33, "Bad passpoint length"

        # set up flag byte
        flag = 0x20 if compressed else 0x0
        if has_lot_seq:
            flag |= 0x04

        seedb = os.urandom(24)
        factorb = Hash(seedb)

        point = ser_to_point(passpoint) * cls._bytes_to_int(factorb)
        pubkey = point_to_ser(point, compressed)
        generatedaddress = pubkey_to_address('p2pkh', pubkey.hex())
        addresshash = Hash(generatedaddress)[:4]

        salt = addresshash + ownerentropy
        derived = cls._scrypt(passpoint, salt=salt, N=1024, r=1, p=1, dkLen=64)

        derivedhalf1 = derived[:32]
        derivedhalf2 = derived[32:]

        h = pyaes.AESModeOfOperationECB(derivedhalf2)

        encryptedpart1 = h.encrypt(bytes( (x[0] ^ x[1]) for x in zip(seedb[:16], derivedhalf1[:16]) ))
        encryptedpart2 = h.encrypt(bytes( (x[0] ^ x[1]) for x in zip(encryptedpart1[8:] + seedb[16:24], derivedhalf1[16:]) ))

        return cls( EncodeBase58Check(bytes((0x01, cls.Type.ECMult, flag)) + addresshash + ownerentropy + encryptedpart1[:8] + encryptedpart2) )


    @staticmethod
    def _int_to_bytes(value, length):
        result = []
        for i in range(0, length):
            result.append(value >> (i * 8) & 0xff)
        result.reverse()
        return bytes(result)

    @staticmethod
    def _bytes_to_int(by):
        result = 0
        for b in by:
            result = result * 256 + int(b)
        return result


    def __repr__(self):
        ret = "<{}:".format(self.__class__.__name__)
        d = dir(self)
        for x in d:
            a = getattr(self, x)
            if not x.startswith('_') and isinstance(a, (int,bytes,bool,str)):
                if x == 'typ':
                    a = self.typeString()
                elif isinstance(a, int) and not isinstance(a, bool):
                    a = '0x' + bh2u(self._int_to_bytes(a,1))
                elif isinstance(a, bytes):
                    a = '0x' + bh2u(a) if a else a
                ret += " {}={}".format(x,a)
        ret += ">"
        return ret

    def __str__(self):
        return self.enc
