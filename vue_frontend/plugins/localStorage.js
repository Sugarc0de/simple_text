import createPersistedState from 'vuex-persistedstate'

export default ({ store }) => {
    createPersistedState({
        // other options...
        storage: sessionStorage,
  })(store)
}
