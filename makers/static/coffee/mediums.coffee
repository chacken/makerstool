class Makers.Medium extends Backbone.RelationalModel
  name: 'Medium'

  constructor: (args) ->
    super(args)

  relations: [
    {
      type: 'HasMany',
      key: 'datapoints',
      relatedModel: 'Makers.DataPoint',
      collectionType: 'Makers.DataPoints',
      createModels: true,
      reverseRelation: {
        key: 'medium',
        includeInJSON: 'id'
      }
    },
    {
      type: 'HasOne',
      key: 'project',
      relatedModel: 'Makers.Project',
      collectionType: 'Makers.Projects',
    }]

  url: =>
    "/mediums/#{this.get(0)}"

Makers.Medium.setup()

class Makers.Mediums extends Backbone.Collection
  model: Makers.Medium

  comparator: (medium) -> medium.get(2)

  reset: (c) ->
    super(c)
    this.sort()

Makers.mediums = new Makers.Mediums()


