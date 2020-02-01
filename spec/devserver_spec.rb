# spec/myapp_spec.rb

require 'dockerspec/serverspec'

describe 'My Dockerfile' do
  describe docker_build('.') do
    it { should have_env 'TZ' }
    it { should have_env 'DEBIAN_FRONTEND' }
    it { should have_cmd ['/usr/bin/zsh', '-'] }
    describe docker_run(described_image) do
      describe 'dotfiles should be set up' do
        describe file('/dotfiles') do
          it { should exist }
          it {should be_directory }
        end
        describe file('/root/.bin') do
          it { should exist }
          it {should be_directory }
        end
      end
      describe 'vim is set up' do
        describe command('vim --version') do
          its(:stdout) { should match('VIM - Vi IMproved 8.2') }
          its(:exit_status) { should eq 0 }
        end
        describe file('/root/.vimrc') do
          it { should exist }
        end
        describe file('/root/.vim') do
          it { should exist }
          it {should be_directory }
        end
        describe file('/root/.vim/autoload/plug.vim') do
          it { should exist }
        end
        describe file ('/usr/local/share/diff-highlight') do
          it { should exist }
        end
        describe 'lang servers work' do
          describe command('solargraph') do
            its(:exit_status) { should eq 0 }
          end
        end
        describe 'coc extensions are installed' do
          describe command('cd /root/.config/coc/extensions; yarn list --pattern coc --depth=0') do
            ['coc-go', 'coc-java', 'coc-json', 'coc-pairs', 'coc-phpls', 'coc-python', 'coc-rls', 'coc-solargraph', 'coc-tsserver', 'coc-yaml'].each do |extension|
              its(:stdout) { should match(extension) }
            end
          end
        end
      end
      describe 'rust works' do
        ['cargo', 'rustc', 'rustc', 'rustdoc', 'rustup'].each do |cmd|
          describe command("/root/.cargo/bin/#{cmd} --version") do
            its (:exit_status) { should eq 0 }
          end
        end
      end
      describe 'packages were installed' do
        ['curl', 'default-jdk', 'git', 'jq', 'nodejs', 'npm', 'php', 'python3',
         'python3-pip', 'tmux', 'wget', 'zsh'].each do |package|
          describe package(package) do
            it { should be_installed }
          end
        end
        ['awscli', 'beautifulsoup4', 'requests'].each do |package|
          describe package(package) do
            it { should be_installed.by('pip') }
          end
        end
      end
      describe 'terraform is installed' do
        describe command('terraform --version') do
          its(:stdout) { should match('v0.12.9') }
          its(:exit_status) { should eq 0 }
        end
      end
      describe 'go is installed' do
        describe file('/usr/local/go/bin') do
          it {should exist }
          it {should be_directory }
        end
        describe command('/usr/local/go/bin/go version') do
          its(:exit_status) { should eq 0 }
          its(:stdout) { should match('go version go1.13') }
        end
      end
    end
  end
end
