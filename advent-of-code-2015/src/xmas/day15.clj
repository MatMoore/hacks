(ns xmas.day15
  (:require [xmas.helpers :refer :all])
)

(def ingredient-regex
  #"(\w+): capacity (-?[0-9])+, durability (-?[0-9])+, flavor (-?[0-9])+, texture (-?[0-9])+, calories (-?[0-9]+)")

(defn parse-line
  [line]
  (let [[match ingredient capacity durability flavor texture calories] (re-find ingredient-regex line)]
    [ingredient (map parse-int [capacity durability flavor texture]) (parse-int calories)]))

(def day15-input (map parse-line (read-lines "day15.txt")))

(defn sum-ingredient
  "Sums all the properties of the mix so far with those of the new ingredient"
  [[chosen-ingredients prev-properties] [ingredient new-properties calories]]
  [(conj chosen-ingredients ingredient) (map + prev-properties new-properties)])

(defn score-mix
  "Score a mix by multiplying its properties - which we arrived at by summing ingredient properties together."
  [[ingredients multiplied-properties]]
  (reduce * (map (partial max 0) multiplied-properties)))

(defn add-a-teaspoon
  "Add one more ingredient to the mix, maximising score."
  [mix possible-ingredients]
  (let [possible-mixes
        (for
          [possible-ingredient possible-ingredients]
          (sum-ingredient mix possible-ingredient))]
    (apply max-key score-mix possible-mixes)))

(defn start-mix
  "This represents our initial mix with 0 ingredients and a sequence of 0s for the properties."
  [possible-ingredients]
  [[] (repeat (count possible-ingredients) 0)])

(defn make-cookie-mix
  "Presumably for part 2 we want to count calaries, but for now we can just keep adding teaspoons as long as it increases the score? NOPE doesn't work

  With a calory constraint it looks a lot like the knapsack problem m[w] = max(v_i + m[w-w_i])
  probably we can build up a map for m."
  [n possible-ingredients]
  (reduce
    (fn [mix i]
      (add-a-teaspoon mix possible-ingredients))
    (start-mix possible-ingredients)
    (range 0 n)))

(defn day15-solution
  []
  [(make-cookie-mix 100 day15-input)])
