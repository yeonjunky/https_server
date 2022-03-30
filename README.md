## reference links
[Enabling HTTPS on Your Servers](https://web.dev/enabling-https-on-your-servers/)
[openssl self signed certification](https://www.baeldung.com/openssl-self-signed-cert)

## goal of this project
- Create a 2048-bit RSA public/private key pair
- Generate a certificate signing request(CSR) that embeds my public key
- Share my SCR with my Certificate Authority (CA) to receive a final certificate or a certificate chain.
- install my final certificate in a non-accessible place such as ```/etc/ssl``` (Linux and Unix)

## What is SSL?
SSL(Secure Socket Layer) is devloped by Netscape.

## Root CA 인증서 생성
CA가 사용할 RSA key pair(public, private key) 생성
```openssl genrsa -out rootca.key 2048```

인증서 요청 생성
```openssl req -new -key rootca.key -out rootca.csr -config rootca_openssl.conf```

인증서 생성
```
openssl x509 -req -days 365 \
-extensions v3_ca \
-set_serial 1 \
-in rootca.csr \
-signkey rootca.key \
-out rootca.crt \
-extfile rootca_openssl.conf
```

## SSl인증서 발급
root ca 서명키로 SSL인증서 발급

키 쌍 생성
```openssl genrsa -out example.key 2048```

개인키 pass phrase 제거

개인키를 보호하기 위해 Key-Derived Function 으로 개인키 자체가 암호화되어 있다. 인터넷 뱅킹등에 사용되는 개인용 인증서는 당연히 저렇게 보호되어야 하지만 SSL 에 사용하려는 키가 암호가 걸려있으면 웹 서버 구동때마다 pass phrase 를 입력해야 하므로 암호를 제거한다.
```
cp  example.key  example.key.enc
openssl rsa -in  example.key.enc -out example.key
```

CSR 파일 생성
```openssl req -new -key example.key -out example.csr -config host_openssl.conf```

인증서 발급
```
openssl x509 -req -days 365 -extensions v3_user -in example.csr \
-CA rootca.crt -CAcreateserial \
-CAkey  rootca.key \
-out example.crt  -extfile host_openssl.conf
```

서버에서 읽을 수 있도록 시스템의 표준 개인키와 인증서 디렉터리에 복사
```
sudo cp example.crt /etc/pki/tls/certs/
sudo cp example.key /etc/pki/tls/private/
```