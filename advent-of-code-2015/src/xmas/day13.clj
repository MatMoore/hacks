(ns xmas.day13
  (:require [xmas.helpers :refer :all])
)

(def input-lines (read-lines "day13.txt"))

(defn parse-line
  [line]
  (let
    [[match a gainlose value b]
     (re-find #"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)" line)]
    (if (= gainlose "lose")
      [[a b] (- 0 (parse-int value))]
      [[a b] (parse-int value)])))

(def preferences
  (reduce
   (fn [acc [pair value]]
     (assoc-in acc [pair] value))
   {}
   (map parse-line input-lines)))

(defn all-splits
  "Each split of the current-seating sequence is a place we could add a new guest."
  [current-seating]
  (for [i (range (count current-seating))]
    (split-at i current-seating)))

(defn get-neighbours-for-split
  "The neighbours are the last of before and the first of after. If either collection is empty, wrap around using the other collection."
  [before after]
  (let
    [cycled (concat after before)]
    [(last cycled) (first cycled)]))

(defn get-cost-for-neighbour
  "Get the cost of separating two guests."
  [prefs [a b]]
  (+
   (prefs [a b])
   (prefs [b a])
   )
  )

(defn get-cost-for-seat
  "Cost of placing a guest between two other guests. Actually this is the opposite of cost. Whoops."
  [prefs [before after] c]
  (let [[a b] (get-neighbours-for-split before after)]
    (-
      (+
        (get-cost-for-neighbour prefs [a c])
        (get-cost-for-neighbour prefs [b c])
      )
     (get-cost-for-neighbour prefs [a b])
     )
    )
  )

(defn best-split
  "Get the best way of splitting the guests already seated."
  [prefs current-seating new-guest]
  (let [min-by-cost (partial max-key #(get-cost-for-seat prefs % new-guest))]
    (apply min-by-cost (all-splits current-seating))))

(defn seat-guest
  "Seat a new guest by trying all possible spaces between those already seated."
  [prefs current-seating new-guest]
  (case (count current-seating)
    0 [new-guest]
    1 (conj current-seating new-guest)
    (let [[before after] (best-split prefs current-seating new-guest)]
      (concat before [new-guest] after))))

(defn guestlist
  "Extract the guests from the preference map."
  [prefs]
  (set (flatten (keys prefs))))

(defn seat-all-guests
  "I don't think this algorithm works in all cases... but it worked for the test input."
  [prefs]
  (reduce (partial seat-guest prefs) [] (guestlist prefs)))

(defn happiness-values
  "Sequence of happiness measurements for each pair of guests."
  [prefs seating-arrangement]
    (for [split (all-splits seating-arrangement)]
      (get-cost-for-neighbour prefs (apply get-neighbours-for-split split)))
    )

(defn happiness-value
  "Total change in happiness for a seating arrangement."
  [prefs seating-arrangement]
  (reduce + (happiness-values prefs seating-arrangement)))

(def second-part
  "When we sit in the middle of two people we neutralise any happiness between them. So we should sit in between the two people that like each other the least."
  (reduce + (drop 1 (sort (happiness-values preferences (seat-all-guests preferences))))))

(defn day13-solution
  []
  [
   (happiness-value preferences (seat-all-guests preferences))
   second-part
  ]
  )
