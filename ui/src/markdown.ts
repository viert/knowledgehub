import showdown from 'showdown'
import showdownHTMLEscape from 'showdown-htmlescape'
import showdownHighlight from 'showdown-highlight'
import XRegExp from 'xregexp'

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
  extensions: [showdownHTMLEscape, showdownHighlight, usernameExt]
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
