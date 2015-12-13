(ns xmas.day13-test
  (:require [clojure.test :refer :all]
            [xmas.day13 :refer :all]))

(deftest test-neighbours
  (is (= (get-neighbours-for-split ['a 'b] ['c 'd])
         ['b 'c]))
  (is (= (get-neighbours-for-split [] ['c 'd])
         ['d 'c]))
  (is (= (get-neighbours-for-split ['a 'b] [])
         ['b 'a]))
  )

(def test-prefs
  {[:a :b] 54,  [:a :c] -79, [:a :d] -2,
   [:b :a] 83,  [:b :c] -7,  [:b :d] -63,
   [:c :a] -62, [:c :b] 60,  [:c :d] 55,
   [:d :a] 46,  [:d :b] -7,  [:d :c] 41})


(deftest test-seat-last
  (is (= (seat-guest test-prefs [:a :b :c] :d) [:d :a :b :c]))
 )

(deftest test-all-splits
  (is (=
       (all-splits [:a :b :c])
       [
        [[] [:a :b :c]]
        [[:a] [:b :c]]
        [[:a :b] [:c]]
       ])))

(deftest test-best-split
  (is (= (best-split test-prefs [:a :b :c] :d) [[] [:a :b :c]]))
 )

(deftest test-seat-guests
  (is (=
       (seat-all-guests test-prefs)
       [:c :d :a :b]))
)

(deftest test-happiness-value
  (is (=
       (happiness-value test-prefs [:c :d :a :b])
       330)))
