class MsaFake(object):

    def __init__(self):
        self.linkage = None
        self.template = None
        self.onChanged = None
        self.updateLinkage = None
        self.settings = {}

    def setModTemplate(self, linkage, template, onChanged):
        self.linkage = linkage
        self.template = template
        self.onChanged = onChanged

    def updateModSettings(self, linkage, newSettings=None):
        self.updateLinkage = linkage
        self.settings = dict(newSettings or {})


msa_fake = MsaFake()
g_modsSettingsApi = msa_fake