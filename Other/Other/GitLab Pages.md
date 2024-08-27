# GitLab Pages

Пример [https://gitlab.com/pages/plain-html/-/tree/main/](https://gitlab.com/pages/plain-html/-/tree/main/)

## **Install Runner**

### **Install Runner Linux**

[https://docs.gitlab.com/runner/install/linux-repository.html](https://docs.gitlab.com/runner/install/linux-repository.html)

To install GitLab Runner:

1. Add the official GitLab repository:
For Debian/Ubuntu/Mint:
`curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash`
2. Install the latest version of GitLab Runner, or skip to the next step to install a specific version:
For Debian/Ubuntu/Mint:
`sudo apt-get install gitlab-runner`
3. [Register a runner](https://docs.gitlab.com/runner/register/index.html).

### **Install Runner for Windows**

[https://devops4solutions.medium.com/setting-up-gitlab-runner-on-windows-d3c46b855ec9](https://devops4solutions.medium.com/setting-up-gitlab-runner-on-windows-d3c46b855ec9)

## Register a runner

**gitlab-runner commands**

`sudo gitlab-runner register --url https://gitlab.com/ --registration-token $REGISTRATION_TOKEN`

`$REGISTRATION_TOKEN` смотреть в GitLab **Menu → Settings → CI/CD → Runners (Expand) → Project runners**

В качестве executor выбирать **docker** c дефолтным образом.

<aside>
❗ Для выполнение инструций через **shell** executor потребуютя sudo права.

</aside>

`sudo gitlab-runner start` 

`sudo gitlab-runner stop`

`sudo gitlab-runner restart`

Включить для runner

![Untitled](GitLab%20Pages/Untitled.png)