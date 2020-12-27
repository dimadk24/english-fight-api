import { createModel } from '../core/model-utils'
import tcomb from 'tcomb'
import { Null } from '../core/tcomb-types'

const props = {
  id: tcomb.Number,
  questionWord: tcomb.String,
  answerWords: tcomb.list(tcomb.String),
  correctAnswer: tcomb.union([Null, tcomb.String]),
  selectedAnswer: tcomb.union([Null, tcomb.String]),
  isCorrect: tcomb.Boolean,
}

export class Question extends createModel(props, 'Question') {}
