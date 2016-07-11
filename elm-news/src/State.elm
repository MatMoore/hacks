module State exposing (..)
import Types exposing (..)
import Rest exposing (..)

init : ( Model, Cmd Msg )
init = ( {news = [], error=Nothing}
        , getNews
    )

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GetNewsResponse (Err errorMessage) ->
            ( { model | error = Just errorMessage }, Cmd.none )
        GetNewsResponse (Result.Ok news) ->
            ( { model | error = Nothing , news=news }, Cmd.none )
        Nope ->
            ( model, Cmd.none )

subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none
