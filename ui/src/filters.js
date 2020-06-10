export function duration(dt) {
  // TODO: singles and plurals
  const moment = new Date(dt).getTime()
  const now = Date.now()

  let dur = Math.floor((now - moment) / 1000)
  if (dur < 60) {
    return `${dur} seconds ago`
  }

  dur = Math.floor(dur / 60)
  if (dur < 60) {
    return `${dur} minutes ago`
  }

  dur = Math.floor(dur / 60)
  if (dur < 24) {
    return `${dur} hours ago`
  }

  if (dur < 24 * 7) {
    return `${Math.floor(dur / 24)} days ago`
  }

  if (dur < 24 * 30) {
    return `${Math.floor(dur / 24 / 7)} weeks ago`
  }

  if (dur < 24 * 365) {
    return `${Math.floor(dur / 24 / 30)} months ago`
  }

  return `${Math.floor(dur / 24 / 365)} years ago`
}
