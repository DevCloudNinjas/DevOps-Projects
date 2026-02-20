# Secrets management and encryption at rest

## Follow along locally

---
## Secrets management and encryption at rest

- Secrets management = selectively and securely bring secrets to services
- Encryption at rest = protect against storage theft or prying
- Remember:
  - control plane is authenticated through mutual TLS, certs rotated every 90 days
  - control plane is encrypted with AES-GCM, keys rotated every 12 hours
  - data plane is not encrypted by default (for performance reasons)

---
## Secret management

- Docker has a "secret safe" (secure key→value store)
- You can create as many secrets as you like
- You can associate secrets to services
- Secrets are exposed as plain text files, but kept in memory only (using `tmpfs`)
- Secrets are immutable (at least in Engine 1.13)
- Secrets have a max size of 500 KB

---
## Creating secrets

- Must specify a name for the secret; and the secret itself


- Assign [one of the four most commonly used passwords](https://www.youtube.com/watch?v=0Jx8Eay5fWQ) to a secret called `hackme`:

```bash
  echo love | docker secret create hackme -
```

If the secret is in a file, you can simply pass the path to the file.

(The special path `-` indicates to read from the standard input.)

---
## Creating better secrets

- Picking lousy passwords always leads to security breaches


- Let's craft a better password, and assign it to another secret:
  ```bash
  base64 /dev/urandom | head -c16 \
   | docker secret create arewesecureyet -
  ```

Note: in the latter case, we don't even know the secret at this point. But Swarm does.

---
## Using secrets

- Secrets must be handed explicitly to services


- Create a dummy service with both secrets:
  ```bash
    docker service create \
           --secret hackme --secret arewesecureyet \
           --name dummy \
           --constraint node.hostname==$HOSTNAME \
           alpine sleep 1000000000
  ```

We constrain the container to be on the local node for convenience.
<br/>
(We are going to use `docker exec` in just a moment!)

---
## Accessing secrets

- Secrets are materialized on `/run/secrets` (which is an in-memory filesystem)
- Find the ID of the container for the dummy service:

```bash
CID=$(docker ps -q --filter label=com.docker.swarm.service.name=dummy)
```

- Enter the container:

```bash
docker exec -ti $CID sh
```

- Check the files in `/run/secrets`

<!-- ```bash grep . /run/secrets/*``` -->
<!-- ```bash exit``` -->

---
## Rotating secrets

- You can't change a secret
  - (Sounds annoying at first; but allows clean rollbacks if a secret update goes wrong)
- You can add a secret to a service with `docker service update --secret-add`
  - (This will redeploy the service; it won't add the secret on the fly)
- You can remove a secret with `docker service update --secret-rm`
- Secrets can be mapped to different names by expressing them with a micro-format:

```bash
docker service create --secret source=secretname,target=filename
```

---
## Changing our insecure password

- Replace our `hackme` secret with a better one
- Remove the insecure `hackme` secret:

```bash
docker service update dummy --secret-rm hackme
```

- Add our better secret instead:

```bash
docker service update dummy \
        --secret-add source=arewesecureyet,target=hackme
```

<small>Wait for the service to be fully updated with e.g. `watch docker service ps dummy`.
<br/>(With Docker Engine 17.10 and later, the CLI will wait for you!)</small>

---
## Checking that our password is now stronger

- Get the ID of the new container:

```bash
CID=$(docker ps -q --filter label=com.docker.swarm.service.name=dummy)
```

- Check the contents of the secret files:

```bash
docker exec $CID grep -r . /run/secrets
```

---
## Secrets in practice

- If you intend to rotate secret `foo`, call it `foo.N` instead, and map it to `foo`
  - N can be a serial, a timestamp...

```bash
docker service create --secret source=foo.N,target=foo ...
```

- You can update (remove+add) a secret in a single command:

```bash
docker service update ... \
  --secret-rm foo.M \
  --secret-add source=foo.N,target=foo
```

---
# Encryption at rest

---

## Encryption at rest

- Swarm data is always encrypted
- A Swarm cluster can be "locked"
- When a cluster is "locked", the encryption key is protected with a passphrase
- Starting or restarting a locked manager requires the passphrase
- This protects against:
  - theft (stealing a physical machine, a disk, a backup tape...)
  - unauthorized access (to e.g. a remote or virtual volume)
  - some vulnerabilities (like path traversal)

---

## Locking a Swarm cluster

- This is achieved through the `docker swarm update` command
- Lock our cluster:

```bash
docker swarm update --autolock=true
```

This will display the unlock key. Copy-paste it somewhere safe.

---

## Locked state

- If we restart a manager, it will now be locked

- Restart the local Engine:

```bash
sudo systemctl restart docker
```
_Note:_ On [Play-With-Docker](http://play-with-docker.com/), you might have to use a different method to restart the Engine.

---

## Checking that our node is locked

- Manager commands (requiring access to crypted data) will fail
- Other commands are OK

- Try a few basic commands:
  ```bash
  docker ps
  docker run alpine echo ♥
  docker node ls
  ```

<!-- ```wait Swarm is encrypted``` -->

(The last command should fail, and it will tell you how to unlock this node.)

---

## Checking node state in scripts

- The state of the node shows up in the output of `docker info`

- Check the output of `docker info`:

```bash
docker info
```

- Can't see it? Too verbose? Grep to the rescue!

```bash
docker info | grep ^Swarm
```

---

## Unlocking a node

- You will need the secret token that we obtained when enabling auto-lock earlier
- Unlock the node:

```bash
docker swarm unlock
```

- Copy-paste the secret token that we got 
- Check that manager commands now work correctly:

```bash
docker node ls
```

---
## Managing the secret key

- If the key is compromised, you can change it and re-encrypt with a new key:

```bash
docker swarm unlock-key --rotate
```

- If you lost the key, you can get it as long as you have at least one unlocked node:

```bash
docker swarm unlock-key -q
```

<small>
_Note:_ if you rotate the key while some nodes are locked, without saving the previous key, those nodes won't be able to rejoin.
<br/> _Note:_ if somebody steals both your disks and your key, <del>you're doomed! Doooooomed!</del>
<br/>you can block the compromised node with `docker node demote` and `docker node rm`.
</small>

---
## Unlocking the cluster permanently

- If you want to remove the secret key, disable auto-lock

- Permanently unlock the cluster:
  ```bash
  docker swarm update --autolock=false
  ```

Note: if some nodes are in locked state at that moment (or if they are offline/restarting
while you disabled autolock), they still need the previous unlock key to get back online.

For more information about locking, you can check the [upcoming documentation](https://github.com/docker/docker.github.io/pull/694).
