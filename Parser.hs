module Parser
  ( parse
  ) where

import qualified Control.Monad (void)
import qualified Text.Megaparsec as Megaparsec
import qualified Text.Megaparsec.Expr as Expr
import qualified Text.Megaparsec.Lexer as L
import qualified Text.Megaparsec.String as MPString

parse :: MPString.Parser ()
parse = L.lexeme L.integer L.space
