FROM ubuntu
# install various programs
ENV DEBIAN_FRONTEND=noninteractive
# additional dependencies at bottom are for building vim
RUN cp /etc/apt/sources.list /etc/apt/sources.list~
RUN sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list
RUN apt-get upgrade && apt-get update && apt-get install -y \
    curl \
    default-jdk \
    git \
    jq \
    nodejs \
    npm \
    php \
    python3 \
    python3-pip \
    tmux \
    wget \
    zsh \
    && apt-get build-dep -y vim
RUN chsh -s /usr/bin/zsh
# install rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
RUN curl -Lo install.sh https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh && sh install.sh --unattended && rm install.sh && mkdir -p /root/.oh-my-zsh/custom/plugins && cd /root/.oh-my-zsh/custom/plugins && git clone https://github.com/softmoth/zsh-vim-mode.git && cd -
# install yarn for coc.nvim extensions
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
	&& echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
	&& apt update \
	&& apt install yarn
# install vim
RUN git clone https://github.com/vim/vim.git \
    && cd vim \
    && ./configure \
    --with-features=huge \
    --enable-pythoninterp \
    --with-python-config-dir \
    && make \
    && make install \
    && cd .. \
    && rm -rf vim
# install vim-plug for vim plugins
RUN curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
        https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
RUN mkdir /root/.bin && git clone https://github.com/sflomenb/dotfiles.git && cd dotfiles && make all && cd ..
# install solargraph for coc-colargraph
RUN gem install solargraph
RUN npm i intelephense -g
# install vim plugins from .vimrc with vim-plug, and coc-extension
RUN vim -c 'PlugInstall | qa' \
    && mkdir -p /root/.config/coc/extensions \
    && cd /root/.config/coc/extensions \
    && if [ ! -f package.json ]; then echo '{"dependencies":{}}'> package.json; fi \
    && yarn add \
    coc-go \
    coc-java \
    coc-json \
    coc-pairs \
    coc-phpls \
    coc-python \
    coc-rls \
    coc-solargraph \
    coc-tsserver \
    coc-yaml
# install pip and various packages
RUN pip3 install --upgrade pip
RUN pip3 install \
    awscli \
    beautifulsoup4 \
    requests
# add diff-highlight
RUN git clone https://github.com/git/git.git official_git \
    && mv official_git/contrib/diff-highlight /usr/local/share/diff-highlight \
    && cd /usr/local/share/diff-highlight \
    && make \
    && sed -i\
        's#/usr/local/share/git-core/contrib/diff-highlight/diff-highlight#/usr/local/share/diff-highlight/diff-highlight#' \
        /root/.gitconfig && cd - \
    && rm -rf official_git
# install terraform
RUN VERSION='0.12.8' \
    && apt-get install unzip \
    && wget https://releases.hashicorp.com/terraform/${VERSION}/terraform_${VERSION}_linux_amd64.zip \
    && unzip terraform_${VERSION}_linux_amd64.zip \
    && mv terraform /usr/local/bin/ \
    && apt-get --purge remove -y unzip \
    && rm terraform_${VERSION}_linux_amd64.zip
# install go
RUN VERSION='1.13' \
    && wget https://dl.google.com/go/go${VERSION}.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go${VERSION}.linux-amd64.tar.gz \
    && rm go${VERSION}.linux-amd64.tar.gz
# set timezone
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
CMD ["/usr/bin/zsh", "-"]
