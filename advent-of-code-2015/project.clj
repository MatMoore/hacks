(defproject xmas "0.1.0-SNAPSHOT"
  :description "Advent of code"
  :dependencies [[org.clojure/clojure "1.7.0"]]
  :main ^:skip-aot xmas.core
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})
