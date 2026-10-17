---
title: "New website"
date: 2026-06-09
slug: new-website
---

So, I *finally* registered a domain - my website now lives at [toonarmycaptain.com](https://toonarmycaptain.com)!

Took a bit of mucking around, but I have it still (for the moment) deployed in the same place on PythonAnywhere.
But I had a lot of trouble with some CSRF stuff.

Turns out the issue was because the Flask-WTF library that I'm using to handle forms checks that the `Origin` header matches its own `hostname`. This ensures that the site submitting to the server isn't a fake, because the client's browser will set the origin as whatever hostname it's seeing (eg `Origin: myfakesite.com`).

The fix was to have my cloudflare proxy rewrite the `Origin`/`Referer` headers sent to the backend to the backend's `hostname`. That way the server is happy because it's not seeing cloudflare as the origin (it's expecting the origin to match its own `hostname`), and the client doesn't know the difference.

```javascript
const origin = headers.get('Origin');                                                                                                                                                       
    if (origin) {                               
        headers.set('Origin', origin.replaceAll(originalHost, targetHost));                                                                                                                     
    }                                                                                                                                                                                         
    const referer = headers.get('Referer');                                                                                                                                                     
    if (referer) {
        headers.set('Referer', referer.replaceAll(originalHost, targetHost));                                                                                                                   
    } 
```
