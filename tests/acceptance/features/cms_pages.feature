Feature: CMS features are provided
  As a visitor of the demo system
  I want to see a few CMS pages showcasing major features of the project
  So that I get a sound impression of the capabilities provided.

  @wip
  Scenario: Welcome page shows navigation, content and sidebar
    Given the demo project has been generated according to the documentation
    When I open the "/" page
    Then a document titled "Home | Organice Demo" is loaded
    And "Welcome to the Organice Demo Site!" is shown as page header
    And "Latest News" is shown as a section header
    And a blog teaser titled "Office Manager" is displayed below
    And the navigation menu has 4 entries: "Home, About Us, Programs, Sponsors"
    And a "calendar" widget is displayed in the "sidebar"

  Scenario: News entry is a clickable teaser
    When I click on the "continue-reading" link of the "Office Manager" teaser
    Then the blog entry "office-manager" titled "Office Manager" is displayed
