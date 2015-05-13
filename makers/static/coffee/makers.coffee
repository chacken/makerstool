window.MakersApp =
  class Makers.Routing extends Backbone.Router
    routes:
      'projects/*subroute': 'projects_module'
      '': ''

    constructor: (params) ->
      super()
      window.Makers.params = params
      #@root = $('#root-content')
      Makers.accounts.reset(params.accounts)
      #console.log(Makers.accounts)
      nav_dropdown = new Makers.ProjectsDropdownView(Makers.accounts).render()
      #console.log($('#projects-dropdown'))
      #$('#projects-dropdown').append(nav_dropdown)

    projects_module: (subroute) =>
      if !Makers.Routers.Projects
        Makers.Routers.Projects = new Makers.ProjectsRouter("projects/")


    #show_project: (id) ->
    #  project = Makers.projects.get(id)
    #  view    = new Makers.ProjectView(project)
    #  @root.empty().append(view.render())
    #  console.log("test")

ProjectOverview =
  init: (params) ->
    root = $('#root-content')
    Makers.mediums.reset(params.mediums)
    project = new Makers.Project(params.project)
    view = new Makers.ProjectView(project).render().el
    root.empty().append(view)

window.ProjectOverview = ProjectOverview






