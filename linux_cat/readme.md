

通过光标移动完成对 cat 内容的隐藏

```sh
echo -e '#!/bin/sh\ncat /etc/passwd\nexit\n\033[A\033[Aecho "Hello dear reader, i am just a harmless script,safe to me!"' > demo.sh
```



Refer https://twitter.com/0xAsm0d3us/status/1774534241084445020

