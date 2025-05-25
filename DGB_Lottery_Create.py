# Tested on python 3.6.5
# GitHub: ReshyResh

import os, binascii, hashlib, base58, ecdsa, urllib.request
def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d
    
for n in range(100000000000):

    priv_key = os.urandom(32)
    fullkey = '80' + binascii.hexlify(priv_key).decode()
    sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
    sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
    WIF = base58.b58encode(binascii.unhexlify(fullkey+sha256b[:8]))
	
	
    add2=fullkey + '01'                                               ##Check for the compressed
    sh1=hashlib.sha256(binascii.unhexlify(add2)).hexdigest()
    sh2=(hashlib.sha256(binascii.unhexlify(sh1)).hexdigest())         ##Double SHA256 for checksum
    compressed=add2+sh2[:8]                                           ##Address+checksum first 4 bytes
    WIF2 = base58.b58encode(binascii.unhexlify(compressed))           ##PKey Compressed
    sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
	
	
    publ_key = '04' + binascii.hexlify(vk.to_string()).decode()       ##Get public key , uncompressed address starts with "D"
    publ_key_comp=binascii.hexlify(vk.to_string()).decode()	          ##Uncomp
    justx=publ_key_comp[:64]
    justy=publ_key_comp[-64:]
    justy2=int(justy, 16)        

	
    if justy2%2==0:                                                   ##Check if y is even or odd
        key_comp='02'+justx                                           ##Prefix 02 if even, 03 if odd, followed by the x
    else:
        key_comp='03'+justx
		
    hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
    hash160_1 = ripemd160(hashlib.sha256(binascii.unhexlify(key_comp)).digest()).digest()
    publ_addr_a1 = b"\x1e" + hash160_1                                ##Prefix for DigiByte
    publ_addr_a = b"\x1e" + hash160
    checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
    checksum1 = hashlib.sha256(hashlib.sha256(publ_addr_a1).digest()).digest()[:4]
    publ_addr_b = base58.b58encode(publ_addr_a + checksum)
    publ_addr_b1 = base58.b58encode(publ_addr_a1 + checksum1)
	
	
    i = n + 1
    print("\n-----------------------------------------")
    print("Private Key                   ", str(i) + ": " + WIF.decode())
    print("DigiByte Address              ", str(i) + ": " + publ_addr_b.decode())
    print("Private Key Compressed        ", str(i) + ": " + WIF2.decode())
    print("DigiByte Address Compressed   ", str(i) + ": " + publ_addr_b1.decode())
    add=publ_addr_b.decode()
    priv=WIF.decode()
    add_comp=publ_addr_b1.decode()
    priv_comp=WIF2.decode()
    if i!= 100000000000:
        try:
            url = urllib.request.urlopen(
                f"https://explorer.digiassets.net/api/addr/{add}/balance")
            url2 = urllib.request.urlopen(
                f"https://explorer.digiassets.net/api/addr/{add_comp}/balance")
            data = int(url.read().decode())
            data2 = int(url2.read().decode())
            trans = data
            trans2 = data2
            if trans != 0 or trans2 != 0:
                loot = "Collisione trovata: "+str(add)+"\nPKey:  "+str(priv)+"\n"+"Compressed: "+str(add_comp)+"\nPKey Compressed:"+str(priv_comp)+"\n"
                print (loot)
                print ("Creating loot.txt...")
                lootxt = open("loot.txt", 'a')
                lootxt.write(loot)
                lootxt.close()			
            print("Balance 1                        ", str(trans)) 
            print("Balance 2                        ", str(trans2))
        except Exception as e:
            print("Error: "+repr(e))
    	    				

