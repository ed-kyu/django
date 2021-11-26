<template>
  <div class="container bg-dark pt-3">
    <review
      v-for="review in allReviews" :key="review.id" :review="review"
      class="mt-1"
      >
      </review>
  </div>
</template>

<script>
import Review from '@/components/Review.vue'
import { mapState } from 'vuex'

export default {
    name: "ReviewList",
    components: {
      Review,
    },
    data() {
      return {
          // reviews: '',
          // movie_json : this.$store.state.movieCards[this.$route.params.id],
          // reviews: this.$store.state.allReviews
      }
    },
    props: {
      movie_json: Object,
    },
    methods: {
  },
  created: function() {
    if (localStorage.getItem('jwt')) {
      // this.getMovieReviews()
      this.$store.dispatch('LoadAllReviews', this.$route.params.id)
    } else {
      this.$router.push({name: 'Login'})
    }
  },
  computed: {
    ...mapState([
      'allReviews'
    ])
  },
}
</script>

<style scoped>


</style>