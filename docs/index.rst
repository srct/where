.. where documentation master file, created by
   sphinx-quickstart on Fri Feb 28 23:38:15 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

where
=====
A water fountain app. This is the documentation for the where RESTful web API. If you don't know what that means check 
out `this article <https://medium.com/@rwilliams_bv/apis-d389aa68104f>`__.

Resources
=========
Point
-----
A point is an abstract representation of a physical location. This includes buildings, water fountains, rooms, etc. A point
stores various attributes, most importantly:

* Location Coordinates: Given as lat, long

* Category: eg. Water Fountain or Building

* Attributes: Special information about this point that varies depending on it's Category

* Parent: The point that this point belongs to (e.g. Water fountains belong to buildings).

.. http:get:: /point/(int:id)
   
   Get a points information by it's `id`.

   **Example request**:

   .. sourcecode:: http

      GET /point/1 HTTP/1.1
      Host: example.com
      Accept: application/json

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
         "attributes": {
            "radius": {
               "value": 2.0
            }
         },
         "category": 2,
         "children": [
            {
               "attributes": {
                  "bottle_filler": {
                     "value": true
                  },
                  "coldness": {
                     "average_rating": 0.5,
                     "num_reviews": 32
                  }
               },
               "category": 1,
               "id": 2,
               "lat": 38.829791,
               "lon": -77.307043,
               "name": null,
               "parent": 1
            }
         ],
         "id": 1,
         "lat": 38.0,
         "lon": -77.0,
         "name": "Johnson Center",
         "parent": null
      }  

   :>json float lat: latitude of the point
   :>json float lon: longitude of the point
   :>json string name: friendly name of the point
   :>json int parent: parent point id
   :>json int id: id of this point
   :>json int category: category id of this point
   :>json list children: the direct children of this point (those that have this point as a parent)
   :>json dict attributes: attributes associated with the category this point belongs to 
   
   :statuscode 200: there is no error
   :statuscode 404: could not find the point given


.. http:post:: /point/
   
   Create a new point.

   **Example request**:

   .. sourcecode:: http

      POST /point/ HTTP/1.1
      Host: example.com
      Content-Type: application/json
      Accept: application/json

      {
         "parent": 1,
         "category": 2,
         "lat": 27.2,
         "lon": 30.3,
         "name": "Some amazing place",
         "attributes": {
            "radius": {
               "value": 3.9
            }
         }
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json
      Location: /point/3/ 

      {
         "attributes": {
            "radius": {
               "value": 3.9
            }
         },
         "category": 2,
         "children": [],
         "id": 3,
         "lat": 27.2,
         "lon": 30.3,
         "name": "Some amazing place",
         "parent": 1
      }

   :>json float lat: latitude of the point
   :>json float lon: longitude of the point
   :>json string name: friendly name of the point
   :>json int parent: parent point id
   :>json int id: id of this point
   :>json int category: category id of this point
   :>json list children: the direct children of this point (those that have this point as a parent)
   :>json dict attributes: attributes associated with the category this point belongs to 
   
   :statuscode 200: there is no error
   :statuscode 404: could not find the point given

.. toctree::
   :maxdepth: 2
   :caption: Contents:



