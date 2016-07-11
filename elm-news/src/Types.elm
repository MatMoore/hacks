module Types exposing (..)
import Http

type FetchedData a = Loading
        | Failed Http.Error
        | Succeed a

type alias Model = {
    news: FetchedData (List News)
}

type Msg
        = Nope |
        GetNewsResponse (Result Http.Error (List News))

type alias News = { headline : String}


