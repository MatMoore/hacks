# West London Xmas Hack Night 2016

This is the Elm team's solution to the [West London Xmas Hack Night, 2016](
https://www.meetup.com/West-London-Hack-Night/events/235596164/).

## Problem
Santa is delivering his presents by throwing them out of his sleigh at random.

We have 3 signals that tell us how far away a present is from a specific location.

Find the presents and direct a robot to pick them up.

## Solution

To triangulate the presents we use some maths we copied from
[http://math.stackexchange.com/a/1033561](http://math.stackexchange.com/a/1033561).

## Game Server
The game server runs at [http://game.clearercode.com](http://game.clearercode.com).

We communicate with it using JSON over a websocket.

Example commands:

```
{"tag":"SetName","contents":"Kris"},
{"tag":"SetColor","contents":"#ff0000"},
{"tag":"Move","contents":{"x":1,"y":-2}}
```

The movement is a vector, and the length doesn't matter (we move at a fixed speed).
