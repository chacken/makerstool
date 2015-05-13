class Makers.ProjectsRouter extends Backbone.SubRoute
  routes:
    '': 'showProjectDashboard'
    ':projectID': 'showProjectOverview'
    ':projectID/trends': 'showProjectTrends'

  initialize: ->
    @$root = $('#root-content')

  showProjectDashboard: =>
    console.log "showprojectdashboard"
    false

  showProjectOverview: (project_id) =>
    Makers.mediums.reset(window.Makers.params.mediums)
    project = Makers.Project.find({id:project_id})
    console.log(project)
    view = new Makers.ProjectOverview(project).render().el
    @$root.empty().append(view)

  showProjectTrends: =>
    Makers.mediums.reset(window.Makers.params.mediums)
    project = new Makers.Project(window.Makers.params.project)
    trend = Makers.mediums.findWhere({type:'trends'})
    view = new Makers.ProjectTrendsView(project, trend).render().el
    @$root.empty().append(view)



class Makers.Account extends Backbone.RelationalModel
  name: 'Account'

  constructor: (args) ->
    super(args)

  relations: [
    {
      type: 'HasMany',
      key: 'webproperties',
      relatedModel: 'Makers.WebProperty',
      collectionType: 'Makers.WebProperties'
    }]

  url: =>
    if this.get('saved') == false
      "/accounts/save/#{this.get('id')}"
    else
      "/accounts/#{this.get('id')}"

Makers.Account.setup()

class Makers.Accounts extends Backbone.Collection
  model: Makers.Account

  comparator: (account) -> account.get("name")

  reset: (c) ->
    super(c)
    #this.sort()

Makers.accounts = new Makers.Accounts()

class Makers.Project extends Backbone.RelationalModel
  name: 'Project'

  constructor: (args) ->
    super(args)

  url: =>
    if this.get('saved') == false
      "/projects/save/#{this.get('id')}"
    else
      "/projects/#{this.get('id')}"

Makers.Project.setup()

class Makers.Projects extends Backbone.Collection
  model: Makers.Project

  comparator: (project) -> project.get("name")

  reset: (c) ->
    super(c)
    #this.sort()

Makers.projects = new Makers.Projects()


class Makers.CreateProjectView extends Backbone.View
  template: JST['projects/create']

  events:
    'click .cancel':   'close'
    'click .submit':   'save'

  constructor: () ->
    super()
    false
    #super(name)

  close: =>
    $(@el).remove()

  save: =>
    id = $("select[name='id']").val()
    Makers.projects.get(id).save()
    this.close()

  render: () ->
    $(@el).empty().append(@template(projects: Makers.projects.where({saved: false})))
    this


class Makers.ProjectOverview extends Backbone.View
  tagName: 'div'
  template: JST['projects/overview']

  constructor: (@project) ->
    super()
    console.log(@project)
    #super(name)

  render: () ->
    $('#page-title').empty().append(@project.get('name'))#.append(@project.get('name'))
    $(@el).empty().append(@template({project: @project, mediums: Makers.mediums}))
    this


class Makers.ProjectTrendsView extends Backbone.View
  tagName: 'div'
  template: JST['projects/trends']

  constructor: (@project, @medium) ->
    super()
    console.log @medium
    #super(name)

  render: () ->
    $('#page-title').empty().append('Trends')#.append(@project.get('name'))
    $(@el).empty().append(@template({project: @project, dps: @medium.get('datapoints')}))
    this


