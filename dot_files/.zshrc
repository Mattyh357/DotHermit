if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Path to your Oh My Zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="powerlevel10k/powerlevel10k"

# Which plugins would you like to load?
plugins=(aliases git history ubuntu systemadmin sudo zsh-autosuggestions zsh-syntax-highlighting auto-notify)

source $ZSH/oh-my-zsh.sh

# User configuration
export EDITOR='nano'

# Aliases
alias i3c="kate ~/.config/i3/config"
alias polyc="kate ~/.config/polybar/config.ini"
alias c="clear"
alias ll="ls -alF --group-directories-first"
alias r="ranger"
alias gcc="XDG_CURRENT_DESKTOP=GNOME gnome-control-center"
alias mcw=". /usr/lib/mc/mc-wrapper.sh"

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
