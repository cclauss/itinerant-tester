workflow "New workflow" {
  on = "push"
  resolves = ["Flake8 command"]
}

action "Flake8 command" {
  uses = "cclauss/GitHub-Action-for-Flake8@master"
  args = "flake8 . --max-line-length=127"
}
