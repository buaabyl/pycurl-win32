cmake -G "NMake Makefiles" -D CMAKE_BUILD_TYPE=Release -D CMAKE_USE_OPENSSL=1 -D CURL_STATICLIB=1 ..\curl-7.33.0

make sure use static link openssl lib with MD!
