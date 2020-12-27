import bridge from '@vkontakte/vk-bridge'
import { ApiService } from '../core/ApiService'
import { User } from '../core/User'

export class AppService {
  static async fetchUserData() {
    const promises = [
      bridge.send('VKWebAppGetUserInfo'),
      ApiService.get('user'),
    ]
    const [vkUserData, apiUserData] = await Promise.all(promises)
    return User.fromObject({
      id: apiUserData.id,
      vkId: apiUserData.vkId,
      firstName: vkUserData.first_name,
      lastName: vkUserData.last_name,
      photoUrl: vkUserData.photo_200,
      score: apiUserData.score,
    })
  }
}
