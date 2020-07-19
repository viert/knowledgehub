export function countable(c: number, single: string, plural: string) {
  if (c % 10 === 1) return `${c} ${single}`
  return `${c} ${plural}`
}

export function duration(dt: Date) {
  // TODO: singles and plurals
  const moment = new Date(dt).getTime()
  const now = Date.now()

  let dur = Math.floor((now - moment) / 1000)
  if (dur < 60) {
    return `${countable(dur, 'second', 'seconds')} ago`
  }

  dur = Math.floor(dur / 60)
  if (dur < 60) {
    return `${countable(dur, 'minute', 'minutes')} ago`
  }

  dur = Math.floor(dur / 60)
  if (dur < 24) {
    return `${countable(dur, 'hour', 'hours')} ago`
  }

  if (dur < 24 * 7) {
    dur = Math.floor(dur / 24)
    return `${countable(dur, 'day', 'days')} ago`
  }

  if (dur < 24 * 30) {
    dur = Math.floor(dur / 24 / 7)
    return `${countable(dur, 'week', 'weeks')} ago`
  }

  if (dur < 24 * 365) {
    dur = Math.floor(dur / 24 / 30)
    return `${countable(dur, 'month', 'months')} ago`
  }

  dur = Math.floor(dur / 24 / 365)

  return `${countable(dur, 'year', 'years')} ago`
}
