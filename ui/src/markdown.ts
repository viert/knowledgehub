import showdown, {
  ShowdownExtension,
  ConverterOptions,
  Converter
} from 'showdown'
import showdownHighlight from 'showdown-highlight'
import XRegExp from 'xregexp'

const htmlEscape = function(): ShowdownExtension[] {
  // This is a typescript-fixed version of
  // https://github.com/phw/showdown-htmlescape
  //
  // This is due to lack of experience in making .d.ts
  // for third-party libraries =)
  //
  return [
    {
      type: 'lang',
      filter: function(
        text: string,
        _converter: Converter,
        options?: ConverterOptions
      ) {
        const codeBlocks: string[] = []

        function hashCodeBlock(code: string) {
          code = '~C' + (codeBlocks.push(code) - 1) + 'C'
          return code
        }

        text += '~0'
        text = text.replace(/(^[ \t]*>([ \t]*>)*)(?=.*?$)/gm, function(
          wholeMatch
        ) {
          wholeMatch = wholeMatch.replace(/>/g, '~Q')
          return wholeMatch
        })
        if (options && options.ghCodeBlocks) {
          text = text.replace(/(^|\n)(```(.*)\n([\s\S]*?)\n```)/g, function(
            wholeMatch,
            m1,
            m2
          ) {
            return m1 + hashCodeBlock(m2)
          })
        }
        text = text.replace(
          /((?:(?:(?: |\t|~Q)*?~Q)?\n){2}|^(?:(?: |\t|~Q)*?~Q)?)((?:(?:(?: |\t|~Q)*?~Q)?(?:[ ]{4}|\t).*\n+)+)((?:(?: |\t|~Q)*?~Q)?\n*[ ]{0,3}(?![^ \t\n])|(?=(?:(?: |\t|~Q)*?~Q)?~0))/g,
          function(wholeMatch, m1, m2, m3) {
            return m1 + hashCodeBlock(m2) + m3
          }
        )
        text = text.replace(/(^|[^\\])((`+)([^\r]*?[^`])\3)(?!`)/gm, function(
          wholeMatch
        ) {
          return hashCodeBlock(wholeMatch)
        })
        text = text.replace(/&/g, '&amp;')
        text = text.replace(/</g, '&lt;')
        text = text.replace(/>/g, '&gt;')
        while (text.search(/~C(\d+)C/) >= 0) {
          const match = parseInt(RegExp.$1)
          let codeBlock = codeBlocks[match]
          codeBlock = codeBlock.replace(/\$/g, '$$$$') // Escape any dollar signs
          text = text.replace(/~C\d+C/, codeBlock)
        }
        text = text.replace(/~Q/g, '>')
        text = text.replace(/~0$/, '')

        return text
      }
    }
  ]
}

const usernameExt = function() {
  const convertUsername = {
    type: 'lang',
    regex: XRegExp(
      String.raw`(^|[^\pL\pN./=?\\])@([.a-z0-9@_-]*[a-z0-9_])`,
      'g'
    ),
    replace: '$1<User username="$2"/>'
  }

  const escapedAt = {
    type: 'lang',
    regex: /\\@/g,
    replace: '@'
  }
  return [convertUsername, escapedAt]
}

const converter = new showdown.Converter({
  strikethrough: true,
  simpleLineBreaks: true,
  simplifiedAutoLink: true,
  ghCodeBlocks: true,
  excludeTrailingPunctuationFromURLs: true,
  extensions: [htmlEscape, showdownHighlight, usernameExt]
})

const plainConverter = function(input: string) {
  const ext = usernameExt()
  input = input.replace('<', '&lt;').replace('>', '&gt;')
  ext.forEach(rule => {
    input = input.replace(rule.regex, rule.replace)
  })
  return input
}

export default converter
export { plainConverter }
