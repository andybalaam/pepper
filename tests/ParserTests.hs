module ParserTests
  ( run
  ) where

import Parser (parse)
import Test.Tasty (testGroup)
import Test.Tasty.HUnit (assertEqual, testCase)

run =
  testGroup
    "Parsing tests"
    [testCase "Parse 1-char string" $ assertEqual [] 3 $ parse ("\"s\"")]
