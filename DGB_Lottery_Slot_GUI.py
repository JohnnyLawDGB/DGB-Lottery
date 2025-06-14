import os
import binascii
import hashlib
import base58
import ecdsa
import urllib.request
import random
import threading
import tkinter as tk


def ripemd160(x: bytes) -> hashlib._hashlib.HASH:
    d = hashlib.new('ripemd160')
    d.update(x)
    return d


def generate_wallet():
    """Generate a random private key and corresponding DigiByte address."""
    priv_key = os.urandom(32)
    fullkey = '80' + binascii.hexlify(priv_key).decode()
    sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
    sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
    wif = base58.b58encode(binascii.unhexlify(fullkey + sha256b[:8])).decode()

    sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    publ_key = '04' + binascii.hexlify(vk.to_string()).decode()
    hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
    publ_addr_a = b"\x1e" + hash160
    checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
    address = base58.b58encode(publ_addr_a + checksum).decode()
    return wif, address


def check_balance(addr: str) -> int:
    url = f"https://explorer.digiassets.net/api/addr/{addr}/balance"
    with urllib.request.urlopen(url) as response:
        return int(response.read().decode())


def main():
    root = tk.Tk()
    root.title("DigiByte Lottery Slot")

    reels = [tk.Label(root, text='D', font=('Helvetica', 32), width=2) for _ in range(3)]
    for r in reels:
        r.pack(side=tk.LEFT, padx=5, pady=10)

    info = tk.Label(root, text='', font=('Helvetica', 12))
    info.pack(pady=10)

    result_var = tk.StringVar(value='Press Spin to start')
    result_label = tk.Label(root, textvariable=result_var)
    result_label.pack(pady=5)

    characters = list('DGB0123456789')

    def spin():
        def animate(count=0):
            for lbl in reels:
                lbl.config(text=random.choice(characters))
            if count < 15:
                root.after(100, animate, count + 1)
            else:
                threading.Thread(target=generate_and_check).start()
        animate()

    def generate_and_check():
        wif, addr = generate_wallet()
        info.config(text=f"Address: {addr}\nPrivKey: {wif}")
        try:
            bal = check_balance(addr)
            result_var.set(f"Balance: {bal}")
        except Exception as exc:
            result_var.set(f"Error: {exc}")

    tk.Button(root, text='Spin', command=spin).pack(pady=10)

    root.mainloop()


if __name__ == '__main__':
    main()
