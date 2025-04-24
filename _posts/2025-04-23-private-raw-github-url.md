---
title: "Programmatically accessing (private) GitHub file URLs"
excerpt: "How to make it easy to access (private) single files from a github.com repo"
---

Given a `repo`, `ref` (like `refs/heads/<branch>` or `refs/tags/<tag>`), and `path`, how do we access the file?

# Public repos

For public repositories this is as easy as `curl https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}`.

# Private repos

For private repositories, it turns out GitHub allows HTTP user/password authentication using a token as the password (and as far as I can tell any username).

```bash
curl https://token:{TOKEN}@raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}
```

## Set it and forget it

Because this is HTTP user/pass auth, you can set it in your `~/.netrc` file, where then it "just works" anywhere!

```bash
# ~/.netrc
machine api.github.com
  login token
  password {TOKEN}
```

(You probably want to generate a PAT that just has `read` access and nothing else, but I'm not your mother, so...)

(Don't forget to `chmod 600 ~/.netrc` so that only you can read it.)

Now you can use `curl https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}` on private repositories and it will "just work"!

# `.netrc` support in automation

- `curl` (as we just saw) supports it
- [Python's `requests`](https://requests.readthedocs.io/en/latest/user/authentication/#netrc-authentication)
- [Python's `httpx`](https://www.python-httpx.org/advanced/authentication/#netrc-authentication)
- (the list goes on...)

# Conclusion

That's it! Happy coding!
