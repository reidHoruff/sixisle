from sniper.snipers import JSCall 

class HideModal(JSCall):
  def _construct(self):
    JSCall._construct(self, 'hide_modal')

