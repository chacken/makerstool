class Makers.WebProperty extends Backbone.RelationalModel
  name: 'WebProperty'

  constructor: (args) ->
    super(args)

  relations: [
    {
      type: 'HasMany',
      key: 'projects',
      relatedModel: 'Makers.Project',
      collectionType: 'Makers.Projects'
    }]

  url: =>
    if this.get('saved') == false
      "/webproperties/save/#{this.get('id')}"
    else
      "/webproperties/#{this.get('id')}"

Makers.WebProperty.setup()

class Makers.WebProperties extends Backbone.Collection
  model: Makers.WebProperty

  comparator: (wp) -> wp.get("name")

  reset: (c) ->
    super(c)
    #this.sort()

Makers.webproperties = new Makers.WebProperties()


