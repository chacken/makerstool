class Makers.ProjectsDropdownView extends Backbone.View
  el: '#projects-dropdown'
  #template: JST['ui/dropdown']

  constructor: (@accounts) ->
    super()
    #@new_view = new Makers.NewProjectDropdownItem()
    #@new_view.on('click', this.new_project, this)
    #@create_view = new Makers.CreateProjectView()

  new_project: ->
    console.log('clicked')
    #view = @create_view.render().el
    #$(@el).append(view)

  add_account: (account) ->
    view = new Makers.NavAccount(account).render().el
    $(@el).append(view)

  render: () ->
    $(@el).empty()
    #.html(@template(title: 'Projects'))
    #accounts = Makers.accounts #.where({saved: true})
    #_.each @accounts, (project) =>
    @accounts.each (account) =>
      @add_account(account)
    #new_btn = @new_view.render().el
    #@$el.append(new_btn) ## append create new project button
    this


class Makers.NavAccount extends Backbone.View
  tagName: 'li'
  template: JST['projects/navAccount']

  events:
    'click .account': 'on_click'

  constructor: (@account) ->
    super()

  on_click: =>
    if !@selected
      @account.get('webproperties').each (property) =>
        view = new Makers.NavWebProperty(property).render().el
        this.$('ul').append(view)
    @selected = true

  render: ->
    $(@el).empty().append(@template(name: @account.get('name')))
    this


class Makers.NavWebProperty extends Backbone.View
  tagName: 'li'
  template: JST['projects/navWebProperty']

  events:
    'click .property': 'on_click'

  constructor: (@webproperty) ->
    super()

  on_click: =>
    if !@selected
      @webproperty.get('projects').each (project) =>
        view = new Makers.NavProject(project).render().el
        $(@el).append(view)
    @selected = true

  render: ->
    $(@el).empty().append(@template(name: @webproperty.get('name')))
    this


class Makers.NavProject extends Backbone.View
  tagName: 'li'
  template: JST['projects/navProject']

  events:
    'click': 'on_click'

  constructor: (@project) ->
    super()

  on_click: =>
    window.location.replace("/projects/#{@project.id}");
    #MakersApp.navigate('projects/#{@project.id}', {trigger: true})

  render: ->
    $(@el).empty().append(@template(name: @project.get('name')))
    this


class Makers.NewProjectDropdownItem extends Backbone.View
  tagName: 'li'
  template: JST['projects/dropdownItem']

  events:
    'click': 'on_click'

  constructor: (@project) ->
    super()

  on_click: ->
    this.trigger('click')
    #@selected = !@selected
    #window.MakersApp.navigate('project/#{@project.id}', {trigger: true})
    false

  render: ->
    $(@el).empty().append(@template(account: '', name: 'New Project', id:0))
    this

