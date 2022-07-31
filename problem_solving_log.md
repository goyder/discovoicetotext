## 2022-07-16/17

* Trying this out on the M1 Mac Pro
    *  Reviewing performance, it appears that I'm not likely to get really good results. [Link.](https://wandb.ai/tcapelle/apple_m1_pro/reports/Deep-Learning-on-the-M1-Pro-with-Apple-Silicon---VmlldzoxMjQ0NjY3) [Second link.](https://www.reddit.com/r/MachineLearning/comments/ut30ck/d_my_experience_with_running_pytorch_on_the_m1_gpu/)
    * I'm rocking a 14" with 8 CPU / 14 GPU cores. 
    * The gist is that PyTorch running on an M1 Pro is, well, not bad. But nothing to write to Moscow about. I might get a 10x speed up by using a 1080TI (which I have).
* I was still keen to try this out, but ran into a few issues:
    * Torch isn't available for Python 3.10
    * PyEnv wouldn't install a new instance of Python
    * Turns out HomeBrew was broken (using an old, Intel-based install method)
    * So I had to remove Homebrew (not simple in itself)
    * And reinstall
    * Also something was broken in my bash/zsh launch scripts, which I had to fix
    * But Visual Studio Code was doing some kind of incorrect recognition, perhaps because it was the Intel version...? Not clear. The install script wouldn't execute in Visual Studio Code Terminal. 
    * Anyway, once I got the launch scripts and Brew installed, I could sort out PyEnv, install the right version of Python, and try installing Nemo. That fell down, not surprisingly – something in there is unhappy about not running on NVidia GPUs.
    * Oh yeah – `Failed to build pynini onnx pesq mecab-python3 tokenizers`. RIP. That's not gonna be a quick fix.
* Whatever – it's all up and running and I could probably do some lightweight PyTorch work locally now if I wanted to.

Anyway, moved onto my Windows PC, which has a 1080TI.

* Linux was busted, won't boot past a black screen. Not sure why. It should boot into Linux; I just moved the drive boot order a month ago and it worked then. No idea why. W/ever.
* Decided I would try WSL. 
    * Issue 1: I had tried WSL ages ago, and apparently the Ubuntu setup was gone but the WSL remained. It turns out that upgrading WSL to WSL 2 was kind of difficult. I had to find some strangely difficult to find docs to make it happen. [link](https://docs.microsoft.com/en-us/windows/wsl/install-manual).
    * Got it sorted, and was very pleased to see I could boot into Ubuntu and do Ubuntu development from Windows. Pretty sick tbh.
    * Issue 2: Ubuntu access. TBH there wasn't anything unusual here. Standard process of getting the right development tools installed. Get things to a point where PyEnv works. I thought there might some WSL issues, but it turns out not.
    * Issue 3: The file system suddenly turned into a "read only file system" during an update, which was because... I was out of disk space! I was running all of this on the first SSD I ever bought as a boot drive, which 128GB. That doesn't cut it anymore! I managed to free up 20GB and rejig some things and reboot WSL which got me moving, but I was concerned that was not enough space. (I was correct.)
    * Issue 4: Internet. I'm doing a lot of updates. I have a janky-ass PCI-E card for internet access, and it was limited to 802.11g (I think? That's surprisingly. Not sure) and it doesn't seem to do *that* consistently, so I'm waiting a lot to download things.
    * Issue 5: CUDA access in WSL2. Lots of updates required here. Updated my drivers, WSL version, Windows version...
        * Windows wouldn't update – some obscure bug. Needed to jiggle a lot of things to get it to update to latest version, apparently required for WSL CUDA access.
        * CUDA wouldn't install in Ubuntu – some kind of glitch in the keys, perhaps specific to WSL. Needed to swap some GPG keys around.

It works for now, but lord it's slow.
Also the drive ran out of space again.
Definitely need to upgrade to make this worthwhile.
