import axios from 'axios'

const instance = axios.create({
  baseURL: 'https://www.halfcoke.cn',
  timeout: 50000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export function request (config) {
  return instance(config)
}
