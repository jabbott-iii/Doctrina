package = "csvstats"
version = "1.0-1"
source = { url = "git+https://example.org/csvstats.git", tag = "v1.0" }
description = {
  summary = "Prints statistics for each column of a CSV file.",
  license = "MIT",
}
dependencies = { "lua >= 5.4" }
build = {
  type = "builtin",
  modules = { csvstats = "src/csvstats.lua" },
  install = { bin = { csvstats = "bin/csvstats" } },
}
