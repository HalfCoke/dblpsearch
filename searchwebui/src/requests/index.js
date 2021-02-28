import axios from "axios";

export function request(config){
  const instance = axios.create({
    baseURL: 'https://halfcoke.cn:5051',
    timeout: 5000,
  })

  return instance(config)
}



