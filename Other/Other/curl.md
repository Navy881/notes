# curl

# Linux

```bash
base64 b95f0eeb-e837-48f0-9e63-ed410438ce74.jpg | curl -XGET -H "Content-Type: application/json" -d @- [http://aiexploitation.svad2.corp/check](http://aiexploitation.svad2.corp/check)
```

# Windows (cmd)

```bash
certutil -encode 1.jpg | curl -XGET -H "Content-Type: application/json" -d "@-" [http://aiexploitation.svad2.corp/check](http://aiexploitation.svad2.corp/check)
```

#