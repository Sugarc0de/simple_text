export default {
  save_json (state, newResults) {
    state.jsonResults = Object.assign(state.jsonResults, newResults)
  },
  save_output (state, oldOutput) {
    state.output = oldOutput
  },
  save_file (state, newFile) {
    state.file = newFile
  },
  save_ocr (state, ocr_results) {
    state.ocr_results = ocr_results
  }

}
