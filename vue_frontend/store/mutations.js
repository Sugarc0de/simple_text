export default {
  save_json (state, newResults) {
    state.jsonResults = Object.assign(state.jsonResults, newResults)
  },
  save_output (state, oldOutput) {
    state.output = oldOutput
  }
}
