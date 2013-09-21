from sniper.snipers import JSCall 

class HideModal(JSCall):
  def __init__(self):
    JSCall.__init__(self, 'hide_modal')

