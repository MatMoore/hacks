module Main exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import WebSocket
import Json.Decode exposing (Decoder, field)
import Json.Encode
import Debug exposing (log)
import Time exposing (every, second)


type alias Model =
    { lastSeen : Maybe Response
    , currentPosition : Vector
    , pendingRequests : List Request
    }


type Msg
    = NewMessage String
    | Tick


type alias Reading =
    { distance : Float
    , position : Vector
    }


type alias Player =
    { name : String
    , position : Vector
    }


type alias Response =
    { gpss : List Reading
    , players : List Player
    }


type Request
    = SetName String
    | SetColor String
    | Move Vector


type alias Vector =
    { x : Float, y : Float }


type Intersection
    = Intersection Vector Vector


type alias Circle =
    { x : Float, y : Float, r : Float }


myName =
    "Elf"


decodeVector : Decoder Vector
decodeVector =
    Json.Decode.map2 Vector
        (Json.Decode.field "x" Json.Decode.float)
        (Json.Decode.field "y" Json.Decode.float)


decodeReading : Decoder Reading
decodeReading =
    Json.Decode.map2 Reading
        (Json.Decode.field "distance" Json.Decode.float)
        (Json.Decode.field "position" decodeVector)


decodePlayer : Decoder Player
decodePlayer =
    Json.Decode.map2 Player
        (Json.Decode.field "name" Json.Decode.string)
        (Json.Decode.field "position" decodeVector)


decodeResponse : Decoder Response
decodeResponse =
    Json.Decode.map2 Response
        (Json.Decode.field "gpss" (Json.Decode.list decodeReading))
        (Json.Decode.field "players" (Json.Decode.list decodePlayer))


readingToCircle reading =
    { x = reading.position.x, y = reading.position.y, r = reading.distance }


readingIntersection : List Reading -> Result String Vector
readingIntersection readings =
    let
        bestIntersection otherCircle point1 point2 =
            if (distanceFromCircle point1 otherCircle) < (distanceFromCircle point2 otherCircle) then
                point1
            else
                point2
    in
        case readings of
            first :: second :: third :: rest ->
                Ok (intersectionPoint (readingToCircle first) (readingToCircle second))
                    |> Result.map (\(Intersection point1 point2) -> bestIntersection (readingToCircle third) point1 point2)

            _ ->
                Err "Wrong number of readings"


encodeVector : Vector -> Json.Encode.Value
encodeVector vector =
    Json.Encode.object
        [ ( "x", Json.Encode.float vector.x )
        , ( "y", Json.Encode.float vector.y )
        ]


encodeRequest : Request -> Json.Encode.Value
encodeRequest request =
    case request of
        SetName string ->
            Json.Encode.object
                [ ( "tag", (Json.Encode.string "SetName") )
                , ( "contents", (Json.Encode.string string) )
                ]

        SetColor colour ->
            Json.Encode.object
                [ ( "tag", (Json.Encode.string "SetColor") )
                , ( "contents", (Json.Encode.string colour) )
                ]

        Move direction ->
            Json.Encode.object
                [ ( "tag", (Json.Encode.string "Move") )
                , ( "contents", encodeVector direction )
                ]


distance c1 c2 =
    sqrt
        ((c1.x - c2.x) * (c1.x - c2.x) + (c1.y - c2.y) * (c1.y - c2.y))


distanceFromCircle point circle =
    abs ((distance point { x = circle.x, y = circle.y }) - circle.r)


intersectionPoint c1 c2 =
    let
        d =
            distance c1 c2

        l =
            ((c1.r * c1.r) - (c2.r * c2.r) + (d * d))
                / (2 * d)

        h =
            sqrt
                ((c1.r * c1.r) - (l * l))

        x1 =
            (l / d) * (c2.x - c1.x) + (h / d) * (c2.y - c1.y) + c1.x

        y1 =
            (l / d) * (c2.y - c1.y) - (h / d) * (c2.x - c1.x) + c1.y

        x2 =
            (l / d) * (c2.x - c1.x) - (h / d) * (c2.y - c1.y) + c1.x

        y2 =
            (l / d) * (c2.y - c1.y) + (h / d) * (c2.x - c1.x) + c1.y
    in
        Intersection (Vector x1 y1) (Vector x2 y2)


main : Program Never Model Msg
main =
    Html.program
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }


echoServer : String
echoServer =
    "ws://game.clearercode.com/"


init : ( Model, Cmd Msg )
init =
    ( { lastSeen = Nothing
      , currentPosition = { x = 0, y = 0 }
      , pendingRequests = [ SetName myName, SetColor "green" ]
      }
    , Cmd.none
    )


findLocation : List Player -> Maybe Vector
findLocation players =
    List.filter (\player -> player.name == myName) players
        |> List.map .position
        |> List.head


sendRequest : Request -> Cmd Msg
sendRequest request =
    encodeRequest request
        |> Json.Encode.encode 0
        |> WebSocket.send echoServer


relativeTo : Vector -> Vector -> Vector
relativeTo origin vector =
    { x = vector.x - origin.x, y = vector.y - origin.y }


defaultRequest =
    SetColor "red"


generateMove : Response -> Model -> ( Model, Cmd Msg )
generateMove { gpss, players } model =
    let
        target =
            readingIntersection gpss

        location =
            log "Currently at" (findLocation players |> Maybe.withDefault { x = 0, y = 0 })

        cmd =
            case Result.map (relativeTo location) target of
                Ok someTarget ->
                    sendRequest (Move (log "going" someTarget))

                Err msg ->
                    let
                        debug =
                            log "OH NO" msg
                    in
                        sendRequest defaultRequest
    in
        ( { model | currentPosition = location, lastSeen = Just { gpss = gpss, players = players } }, cmd )


update : Msg -> Model -> ( Model, Cmd Msg )
update message model =
    case message of
        Tick ->
            case ( model.pendingRequests, model.lastSeen ) of
                ( request :: rest, _ ) ->
                    ( { model | pendingRequests = rest }, sendRequest request )

                ( _, Just response ) ->
                    generateMove response model

                _ ->
                    ( model, Cmd.none )

        NewMessage str ->
            case Json.Decode.decodeString decodeResponse str of
                Ok response ->
                    ( { model | lastSeen = Just response }, Cmd.none )

                Err msg ->
                    let
                        debug =
                            log "aaaah" msg
                    in
                        ( model, Cmd.none )


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch
        [ WebSocket.listen echoServer NewMessage
        , every second (\t -> Tick)
        ]


view : Model -> Html Msg
view model =
    div []
        [ model |> toString |> text ]
