import axios from 'axios'

export function getBookByID(id) {
    return axios
      .get(`/api/book?id=${id}`)
      .then(res => res.data)
  }
