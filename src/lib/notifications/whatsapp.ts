export interface WhatsAppConfig {
  apiKey: string
  instanceId: string
  baseUrl: string
}

export class WhatsAppService {
  private config: WhatsAppConfig

  constructor(config: WhatsAppConfig) {
    this.config = config
  }

  async sendNotification(phone: string, message: string): Promise<{ success: boolean; error?: string }> {
    if (!this.config.apiKey || !this.config.instanceId) {
      console.error('WhatsApp configuration missing')
      return { success: false, error: 'Configuração do WhatsApp ausente' }
    }

    try {
      const response = await fetch(`${this.config.baseUrl}/message/sendText/${this.config.instanceId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': this.config.apiKey,
        },
        body: JSON.stringify({
          number: phone,
          options: {
            delay: 1200,
            presence: 'composing',
          },
          textMessage: {
            text: message,
          },
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || 'Erro ao enviar mensagem via WhatsApp')
      }

      return { success: true }
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : 'Erro desconhecido ao enviar WhatsApp'
      console.error('WhatsApp Send Error:', errorMessage)
      return { success: false, error: errorMessage }
    }
  }
}

export const whatsappService = new WhatsAppService({
  apiKey: process.env.WHATSAPP_API_KEY || '',
  instanceId: process.env.WHATSAPP_INSTANCE_ID || '',
  baseUrl: process.env.WHATSAPP_BASE_URL || 'http://localhost:8080',
})
