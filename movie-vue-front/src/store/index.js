import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import axios from 'axios'

Vue.use(Vuex)
const SERVER_URL = process.env.VUE_APP_SERVER_URL
// import router from '@/router'

export default new Vuex.Store({
  state: {
    movieCards: [],
    genres: [],
    authUser: '',
    myReviews: [],
    allReviews: [],
    allComments: [],
    rate: '',
    recommendCards: [],
  },
  mutations: {
    LOAD_RECOMMEND_MOVIES: function (state, results) {
      // console.log(results)
      state.recommendCards = results
    },
    LOAD_MOVIE_CARDS: function (state, results) {
      // console.log(results)
      state.movieCards = results
    },
    LOAD_GENRES_NAMES: function (state, results) {
      state.genres = results
    },
    SAVE_AUTH_USER: function(state, result) {
      state.authUser = result
    },
    LOAD_ALL_REVIEWS: function (state, results) {
      state.allReviews = results
    },
    LOAD_ALL_COMMENTS: function (state, results) {
      state.allComments = results
    },
    LOAD_MY_REVIEWS: function (state, results) {
      state.myReviews = results
    },
    ADD_MY_REVIEW: function (state, results) {
      state.myReviews.push(results)
    },
    LOAD_USER_ID: function(state, result) {
      state.authUser = result
    },
    LOAD_RATE: function(state, result) {
      state.rate = result
    },
    UPDATE_COMMENTS(state, comments) {
      state.comments = comments
    },
    UPDATE_COMMENT(state, newComment) {
      console.log(newComment)
      const oldComment = state.comments.find(comment => comment.id === newComment.id)
      
      for (const key in oldComment) {
        oldComment[key] = newComment[key]
      }
    },
    UPDATE_REVIEW(state, newReview) {
      console.log(newReview)
      const oldReview = state.reviews.find(review => review.id === newReview.id)
      
      for (const key in oldReview) {
        console.log(key)
        oldReview[key] = newReview[key]
      }
    },
    UPDATE_RATE(state, newRate) {
      console.log(newRate)
      const oldRate = state.reviews.find(rate => rate.id === newRate.id)
      
      for (const key in oldRate) {
        oldRate[key] = newRate[key]
      }
    },
    UPDATE_REVIEWS(state, reviews) {
      state.reviews = reviews
    },
  },
  actions: {
    LoadRecommendMovies: function ({commit}) {
      axios({
        method: 'get',
        url: `${SERVER_URL}/accounts/${this.state.authUser.username}/recommendbyprofile/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
      })
        .then((res) => {
          // console.log(res)
          commit('LOAD_RECOMMEND_MOVIES', res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
    LoadMovieCards: function ({commit}) {
      axios({
        method: 'get',
        url: `${SERVER_URL}/movies/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
      })
        .then((res) => {
          // console.log(res)
          commit('LOAD_MOVIE_CARDS', res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
    LoadGenresNames: function ({commit}) {
      axios({
        method: 'get',
        url: `${SERVER_URL}/movies/genres/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
      })
        .then((res) => {
          // console.log(res)
          commit('LOAD_GENRES_NAMES', res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
    SaveAuthUser: function ({commit}, username) {
      commit('SAVE_AUTH_USER', username)
    },
    LoadMyReviews: function ({commit},) { // {commit}, user_pk
      axios({
        method: 'get',
        url: `${SERVER_URL}/myreviews/2/`, // 수정바람
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
      })
        .then((res) => {
          // console.log(res)
          commit('LOAD_MY_REVIEWS', res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
    LoadAllReviews: function ({commit}, movie_pk) {
      axios({
        method: 'get',
        url: `${SERVER_URL}/reviews/movies/${movie_pk}/`, 
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
      })
        .then((res) => {
          console.log(res)
          commit('LOAD_ALL_REVIEWS', res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
    LoadAllComments: function ({commit}, review_pk) {
      axios({
        method: 'get',
        url: `${SERVER_URL}/reviews/${review_pk}/comments/`, 
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
      })
        .then((res) => {
          // console.log(res)
          commit('LOAD_ALL_COMMENTS', res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
    LoadRate: function ({commit}, movie_pk) {
      axios({
        method: 'get',
        url: `${SERVER_URL}/reviews/movies/${movie_pk}/${this.state.authUser.id}/`, 
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
      })
        .then((res) => {
          console.log('load rate', res)
          commit('LOAD_RATE', res.data)
        })
        .catch(err => {
          this.state.rate = null,
          console.log(err)
        })
    },
    AddMyReview({ commit }, review, movie_pk) {
      // commit('ADD_MY_REVIEW', review)
      axios({
        method: 'post',
        url: `${SERVER_URL}/reviews/movies/${movie_pk}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
        
      })
        .then((res) => {
          // console.log(res)
          commit('ADD_MY_REVIEW', res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
    LoadUserId({commit}) {
      axios({
        method: 'GET',
        url: `${SERVER_URL}/accounts/identify/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`},
      })
      .then(res => {
        console.log(res)
        commit('LOAD_USER_ID',res.data)
      })
      .catch(err => {
        console.log(err)
      })
    },
    async FetchComments({ commit }) {
      const res = await fetch(URL)
      const comments = await res.json()
      commit('UPDATE_COMMENTS', comments)
    },
    async FetchReviews({ commit }) {
      const res = await fetch(URL)
      const reviews = await res.json()
      commit('UPDATE_REVIEWS', reviews)
    },
    UpdateComment({ commit }, newComment) {
      axios({
        method: 'PUT',
        url: `${SERVER_URL}/reviews/comments/${newComment.id}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`},
        data: {
          content: newComment.content
        }
      })
      .then(res => {
        console.log(res)
        commit('UPDATE_COMMENT', newComment)
      })
      .catch(err => {
        console.log(err)
      })
    },
    UpdateReview({ commit }, newReview) {
      axios({
        method: 'PUT',
        url: `${SERVER_URL}/reviews/${newReview.id}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`},
        data: {
          title: newReview.title,
          content: newReview.content,
          rate: newReview.rate,
        }
      })
      .then(res => {
        console.log(res)
        commit('UPDATE_REVIEW', newReview)
      })
      .catch(err => {
        console.log(err)
      })
    },
    UpdateRate({ commit }, newRate) {
      axios({
        method: 'PUT',
        url: `${SERVER_URL}/rates/${newRate.id}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`},
        data: {
          rate: newRate.rate,
        }
      })
      .then(res => {
        console.log(res)
        commit('UPDATE_RATE', newRate)
      })
      .catch(err => {
        console.log(err)
      })
    },
    // uploadImages({ commit }, event) {
    //   const { token } = commit.auth
    //   const images = Array.from(event.target.files)
    //   const config = {
    //     headers: { 
    //       'Authorization': `JWT ${token}`, 
    //     },
    //   }
  
    //   const promises = []
    //   images.forEach(image => {
    //     const formData = new FormData()
    //     formData.append('image', image)
  
    //     const p = axios.post(UPLOAD_URL, formData, config)
    //     promises.push(p)
    //   })
  
    //   Promise.all(promises)
    //     .then(() => router.push({name: 'Home'}))
    //     .catch(err => console.error(err))
    // }
  },
  modules: {
  },
  plugins: [
    createPersistedState(),
  ]
})