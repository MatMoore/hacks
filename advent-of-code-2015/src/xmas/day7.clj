(ns xmas.day7
  (:require [xmas.helpers :refer :all])
)

(def wire-funcs
  {"OR" bit-or
   "AND" bit-and
   "NOT" bit-not
   "RSHIFT" unsigned-bit-shift-right
   "LSHIFT" bit-shift-left})

(defn truncate-16-bits
  "Bitwise functions return longs. We only care about the bottom 16 bits"
  [n]
  (bit-and n 0xffff))

(defn parse-argument
  [token]
  (try
    [:value (parse-int token)]
    (catch java.lang.NumberFormatException e [:symbol token])))

(defn parse-expression
  [line]
  (let
    [[match lhs rhs] (re-find #"(.*) -> (.*)" line)
     [opmatch left op right] (re-find #"(\w+)?\s*(AND|OR|RSHIFT|LSHIFT|NOT)\s+(\w+)" lhs)]
    (if (nil? opmatch)
      [rhs (parse-argument lhs)]
      (if (nil? left)
        [rhs [:expression [(get wire-funcs op)
                           [(parse-argument right)]]]]
        [rhs [:expression [(get wire-funcs op)
                           [(parse-argument left) (parse-argument right)]]]]))))

(def day7-data
  (with-open [rdr (clojure.java.io/reader "day7.txt")]
    (into {} (map parse-expression (line-seq rdr)))))

(declare evaluate-wires)

(defn evaluate-argument
  "Take a signal measurement (this is a either a literal or a symbol lookup)"
  [wires [form value]]
  (case form
    :value value
    :symbol (evaluate-wires wires value)))

(def evaluate-argument-memo
  "Memoize all measurements or we'll be here forever"
  (memoize evaluate-argument))

(defn evaluate-expression
  "Evaluate an expression consisting of a function and some subexpressions.
  In this problem we don't have any nesting so subexpressions can only be literals or symbols."
  [wires [op args]]
  (let [subexprs (map #(evaluate-argument-memo wires %) args)]
    (truncate-16-bits (apply op subexprs))))

(defn evaluate-wires
  "Given the wiring structure and the name of a wire, measure the signal of that wire"
  [wires wire-name]
  (let [[form value] (get wires wire-name)]
    (do
      (println wire-name form value)
      (case form
        :symbol (evaluate-wires wires value)
        :value value
        :expression (evaluate-expression wires value)
        (println (str "miss " wire-name))))))

(def day7-data2
  "For part two we set wire b to the result of part 1"
  (assoc-in day7-data ["b"] [:value 956]))

(defn wire-a
  []
  (evaluate-wires day7-data "a"))

(defn wire-a2
  []
  (evaluate-wires day7-data2 "a"))

(defn day7-solution
  []
  [(wire-a) (wire-a2)]
)
