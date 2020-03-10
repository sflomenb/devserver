#!/bin/bash

set -eu

export DEBIAN_FRONTEND=noninteractive

UPGRADE_PACKAGES=${1:-none}

if [ "${UPGRADE_PACKAGES}" != "none" ]; then
    echo "==> Updating and upgrading packages ..."

    # Add third party repositories
    sudo add-apt-repository ppa:jonathonf/vim -y

    sudo apt-get update
    sudo apt-get upgrade -y
fi

sudo apt-get install -qy \
    curl \
    default-jdk \
    git \
    jq \
    libz-dev \
    maven \
    nodejs \
    npm \
    perl \
    perl-doc \
    php \
    python3 \
    python3-pip \
    python3-venv \
    ruby-dev \
    rubygems \
    shellcheck \
    stow \
    tmux \
    tree \
    unzip \
    vim-gtk3 \
    wget \
    yarn \
    zsh

rm -rf /var/lib/apt/lists/*

[[ ${SHELL} =~ zsh ]] || chsh -s /usr/bin/zsh

if ! [[ -d ~/.oh-my-zsh ]]; then
    curl -Lo install.sh https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh
    sh install.sh --unattended
    rm -f install.sh
fi

if ! [[ -d ~/.oh-my-zsh/custom/plugins ]]; then
    mkdir -p ~/.oh-my-zsh/custom/plugins
    pushd ~/.oh-my-zsh/custom/plugins
    git clone https://github.com/softmoth/zsh-vim-mode.git
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git
    git clone https://github.com/zsh-users/zsh-autosuggestions.git
    popd
fi

if ! [[ -f ~/.vimrc ]]; then
    git clone https://github.com/sflomenb/dotfiles.git
    pushd dotfiles
    make all
    popd
fi

! [[ -x "$(command -v solargraph)" ]] && gem install solargraph
! [[ -x "$(command -v vue)" ]] && npm i -g @vue/cli
! [[ -x "$(command -v bash-language-server)" ]] && npm i -g bash-language-server
! [[ -x "$(command -v intelephense)" ]] && npm i -g intelephense
! [[ -x "$(command -v docker-langserver)" ]] && npm install -g dockerfile-language-server-nodejs

if ! [[ -f ~/.vim/autoload/plug.vim ]]; then
    curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
        https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
    vim -c 'PlugInstall | qa'
    mkdir -p ~/.config/coc/extensions
    pushd ~/.config/coc/extensions
    if [ ! -f package.json ]; then echo '{"dependencies":{}}'> package.json; fi
    yarn add \
        coc-go \
        coc-java \
        coc-json \
        coc-pairs \
        coc-phpls \
        coc-python \
        coc-rust-analyzer \
        coc-solargraph \
        coc-tsserver \
        coc-yaml
    popd
fi

if ! [[ -x "$(command -v rustc)" ]]; then
    curl "https://sh.rustup.rs" -sSf | sh -s -- -y
fi

if ! [[ -x "$(command -v terraform)" ]]; then
    export VERSION='0.12.9'
    wget "https://releases.hashicorp.com/terraform/${VERSION}/terraform_${VERSION}_linux_amd64.zip"
    unzip "terraform_${VERSION}_linux_amd64.zip"
    chmod +x terraform
    mv terraform /usr/local/bin/
    rm -f "terraform_${VERSION}_linux_amd64.zip"
    unset VERSION
fi

if ! [[ -x "$(command -v go)" || -x "/usr/local/go/bin" ]]; then
    export VERSION='1.14'
    wget "https://dl.google.com/go/go${VERSION}.linux-amd64.tar.gz"
    tar -C /usr/local -xzf "go${VERSION}.linux-amd64.tar.gz"
    rm -f go${VERSION}.linux-amd64.tar.gz
    export PATH="/usr/local/go/bin:$PATH"
    unset VERSION
fi

if ! [[ -x "$(command -v kubectl)" ]]; then
    curl -L -o /usr/local/bin/kubectl https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
    chmod 755 /usr/local/bin/kubectl
fi

if ! [[ -x "$(command -v aws)" ]]; then
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm -f awscliv2.zip
fi

# add diff-highlight
if ! [[ -x "/usr/local/share/diff-highlight" ]]; then
    git clone https://github.com/git/git.git official_git
    mv official_git/contrib/diff-highlight /usr/local/share/diff-highlight
    pushd /usr/local/share/diff-highlight
    make
    popd
    rm -rf official_git
    export PATH="${PATH}:/usr/local/share/diff-highlight"
fi

export TZ=America/New_York
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
echo $TZ > /etc/timezone

