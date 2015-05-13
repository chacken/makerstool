class Makers.DataPoint extends Backbone.RelationalModel
  name: 'DataPoint'

  constructor: (args) ->
    super(args)

  url: =>
    "/datapoints/#{this.get(0)}"

Makers.DataPoint.setup()

class Makers.DataPoints extends Backbone.Collection
  model: Makers.DataPoint

  comparator: (dp) -> dp.get(2)

  reset: (c) ->
    super(c)
    this.sort()

Makers.datapoints = new Makers.DataPoints()


